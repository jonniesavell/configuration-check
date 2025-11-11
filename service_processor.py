import subprocess


class SystemDServiceProcessor:
    def process(self, dictionary):
        name = dictionary['name']
        attributes = dictionary['attributes']

        if attributes.get('service') is None:
            raise RuntimeError(f'{name}: missing service metadata')
        else:
            service = attributes['service']

            if attributes.get('state') is None:
                raise RuntimeError(f'{name}: missing state metadata')
            else:
                state = attributes['state']

                if state not in ['enabled', 'running']:
                    raise RuntimeError(f'{name}: invalid state {state}')
                else:
                    if state == 'enabled':
                        enabled = subprocess.run(
                            ['systemctl', 'is-enabled', '--quiet', service]
                        ).returncode == 0

                        if not enabled:
                            raise ValueError(f'{name}: {service}: state not enabled')
                    else:
                        # state == 'running'
                        running = subprocess.run(
                            ['systemctl', 'is-active', '--quiet', service]
                        ).returncode == 0

                        if not running:
                            raise ValueError(f'{name}: {service}: state not running')

        return None
