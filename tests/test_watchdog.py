import pytest
import subprocess
import testinfra
import os

WATCHDOG_PATH = '/tmp/test/files/watchdog.sh'

# scope='session' uses the same container for all the tests;
# scope='function' uses a new container per test function.
@pytest.fixture(scope='function')
def host(request):
    
    docker_id = subprocess.check_output(
        ['docker', 'run', '-d', '--rm', '--mount', 'type=bind,source='+os.getcwd()+',target=/tmp/test', 'centos', 'sleep', '1d']
    ).decode().strip()
 
    # return a testinfra connection to the container
    
    host = testinfra.get_host("docker://" + docker_id)
    host.run('chmod +x {}'.format(WATCHDOG_PATH))
    yield host

    subprocess.check_call(['docker', 'rm', '-f', docker_id])

def test_test_command_is_executed_every_max_duration_seconds(host):
    result = host.run('CMD_TEST_MAX_DURATION=2s CMD_TEST="echo oi" timeout 5s {}'.format(WATCHDOG_PATH))

    assert result.stdout == "oi\noi\noi\n"

def test_when_command_to_test_takes_longer_than_max_duration_then_execute_the_fail_command_and_show_fail_message(host):
    
    result = host.run('CMD_TEST_MAX_DURATION=2s CMD_TEST="sleep 3s" CMD_FAIL="echo fail" MSG_FAIL="failure" timeout 5s {}'.format(WATCHDOG_PATH))

    assert result.stdout == 'failure\nfail\nfailure\nfail\n'

def test_when_command_to_test_takes_less_than_max_duration_then_execute_the_ok_command(host):
    
    result = host.run('CMD_TEST_MAX_DURATION=2s CMD_TEST="sleep 1s" CMD_OK="echo ok" timeout 5s {}'.format(WATCHDOG_PATH))

    assert result.stdout == 'ok\nok\n'

def test_when_command_to_test_takes_the_same_time_of_max_duration_then_execute_the_ok_command(host):
    
    result = host.run('CMD_TEST_MAX_DURATION=2s CMD_TEST="sleep 1s" CMD_OK="echo ok" timeout 5s {}'.format(WATCHDOG_PATH))

    assert result.stdout == 'ok\nok\n'