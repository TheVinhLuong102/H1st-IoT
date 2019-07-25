import boto3
import requests
import sys
import time
import traceback


def get_info(yarn_cluster_name):
    # *** this assumes default port and internal DNS setup ***
    response = \
        requests.get(
            'http://{host}:{port}/ws/v1/cluster/info'.format(
                host="{}.arimo.internal".format(yarn_cluster_name),
                port=8088),
            timeout=30)

    if response.ok:
        return response.json()


def get_instances(yarn_cluster_name):
    # *** this assumes US-EAST-1 region ***
    ec2 = boto3.resource('ec2', region_name='us-east-1')

    return ec2.instances.filter(
            Filters=[{'Name': 'tag:pi-cluster',
                      'Values': [yarn_cluster_name]}])


def start(yarn_cluster_name=None, dontdo=False):
    if (not dontdo) and \
            yarn_cluster_name and \
            isinstance(yarn_cluster_name, str) and \
            (yarn_cluster_name.lower() not in ('none', 'null')):
        instances = get_instances(yarn_cluster_name)
        for instance in instances:
            if instance.state.get('Name') == 'stopping':
                print("%s: Waiting until stopped" % instance)
                instance.wait_until_stopped()

        for instance in instances:
            print("%s: Starting" % instance)
            instance.start()


def stop(yarn_cluster_name=None, dontdo=False):
    if (not dontdo) and \
            yarn_cluster_name and \
            isinstance(yarn_cluster_name, str) and \
            (yarn_cluster_name.lower() not in ('none', 'null')):
        for instance in get_instances(yarn_cluster_name):
            print("%s: Stopping" % instance)
            instance.stop()


def wait_for_instances(yarn_cluster_name=None, dontdo=False):
    if (not dontdo) and \
            yarn_cluster_name and \
            isinstance(yarn_cluster_name, str) and \
            (yarn_cluster_name.lower() not in ('none', 'null')):
        print("Waiting for instances to start")
        for instance in get_instances(yarn_cluster_name):
            print("%s: Waiting until running" % instance)
            instance.wait_until_running()
        print("All instances are running")


def backoff(n):
    return min(0.5 * (2 ** n), 30)


def wait_for_yarn(yarn_cluster_name=None, dontdo=False):
    if (not dontdo) and \
            yarn_cluster_name and \
            isinstance(yarn_cluster_name, str) and \
            (yarn_cluster_name.lower() not in ('none', 'null')):
        print('Waiting for YARN to be ready...')

        begin = time.time()

        for i in range(10):
            try:
                info = get_info(yarn_cluster_name)

            except requests.ConnectionError as e:
                print(e)
                pass

            except Exception:
                traceback.print_exc()
                pass

            else:
                if info.get('clusterInfo', {}).get('state') == 'STARTED':
                    print('YARN is ready')
                    break

                else:
                    print('YARN is not ready')
                    print(info)

            time.sleep(backoff(i))

        else:
            raise Exception('Waited too long for YARN: {} seconds',format(time.time() - begin))

        # give some more time for other resources to be ready (e.g. HDFS).
        print('Sleeping for 30s more for the cluster to be completely ready...')
        time.sleep(30)


def main():
    args = sys.argv[1:]
    assert len(args) == 3
    action, yarn_cluster_name, dontdo = args
    dontdo = bool(int(dontdo))

    if action == 'start':
        start(yarn_cluster_name=yarn_cluster_name, dontdo=dontdo)
        wait_for_instances(yarn_cluster_name=yarn_cluster_name, dontdo=dontdo)
        wait_for_yarn(yarn_cluster_name=yarn_cluster_name, dontdo=dontdo)

    elif action == 'stop':
        stop(yarn_cluster_name=yarn_cluster_name, dontdo=dontdo)

    else:
        raise Exception('Unknown Action {}'.format(action))


if __name__ == '__main__':
    main()
