#!/usr/bin/env python3
# imports
import os
import click
import pathlib as plib
import configparser

# global vars
config = configparser.ConfigParser()
home_dir = plib.Path.home()
aws_root_dir = f'{home_dir}/.aws'
aws_conf_path = f'{aws_root_dir}/config'
aws_cred_path = f'{aws_root_dir}/credentials'

# Functions
@click.command()
@click.option('--initial_setup', is_flag = True, help = 'First time setup for configuration and credentials files in ~/.aws')
@click.option('--mfa', is_flag = True)


def cli(mfa, initial_setup):
    '''Doing checks, building profile, and installing necessary things'''
    click.echo('Bleep Bloop')

    if initial_setup:
        setup_output = check_aws_path()
        click.echo(setup_output)
        
        aws_cli_profile_provided = input('Create a new profile name for CLI: ')
        aws_cli_region_provided = input('Default region for profile: ')
        aws_access_key_provided = input('Acess Key from Management Console: ')
        aws_secret_key_provided = input('Secret Key from Management Console: ')
        aws_mfa_arn_provided = input('MFA ARN from Management Console: ')
       
        create_config = usr_aws_config_setup(aws_cli_profile_provided, aws_cli_region_provided)
        create_config = usr_aws_creds_setup(aws_cli_profile_provided, aws_access_key_provided, aws_secret_key_provided)
        set_mfa_arn = usr_mfa_setup(aws_cli_profile_provided, aws_mfa_arn_provided)
    
    if mfa:
        profile = input('Profile: ')
        mfa_token = input('MFA Token: ')
        session_tokens = usr_mfa_fetch(profile, mfa_token)

def check_aws_path():
    '''
    Checks if configuration and credentials file exists, if it does, then you get a warning
    if it does not, then the files are created and your input is accepted and placed in the appropriate files
    '''
    
    click.echo(f'Checking for AWS root directory `~/.aws` before continuing')
    
    aws_path_check = os.path.exists(f'{aws_root_dir}')
    aws_conf_check = os.path.exists(f'{aws_conf_path}')
    aws_cred_check = os.path.exists(f'{aws_cred_path}')
    
    if aws_path_check: 
        aws_check_message = click.echo(f'Success: AWS CLI directory check passed, path = `{aws_root_dir}`')
    else:
        usr_accept_inst_awscli = input('So the AWS CLI doesn\'t seem to be installed in your user directory\nInstall CLI?')
        
        if usr_accept_instawscli == lower("yes"):
            install_awscli = aws_cli_install()
    
    if aws_conf_check is False and aws_cred_check is False:
        setup_file_message = click.echo('Success: Config and Credentials are not setup, moving on to user setup')
    else:
        setup_file_message = click.echo('We got conflicts, continuing with initial setup will overwrite your configuration and credentials file')
        usr_accept_warning = input('You good with overwriting?')
        
        if usr_accept_warning:
            click.echo('Right-o, continuing')

def aws_cli_install():
    return 'This is a placeholder'

def usr_aws_config_setup(profile, region):
    config[profile] = {
            'output': 'json',
            'region': region
            }
    with open(f'{aws_conf_path}', 'w') as config_file:
        config.write(config_file)
    click.echo('config file created in ~./aws')

def usr_aws_creds_setup(profile, access_key, secret_key):
    config[profile] = {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key
            }
    with open(f'{aws_cred_path}', 'w') as creds_file:
        config.write(creds_file)
    click.echo('credentials file created in ~/.aws')

def usr_mfa_setup(profile, mfa_arn):
    config[profile] = {
            'mfa_arn': mfa_arn
            }

    with open(f'{aws_root_dir}/mfa_arn.conf', 'w') as mfa_file:
        config.write(mfa_file)
    click.echo('mfa_arn.conf file created in ~/.aws')

def usr_mfa_fetch(profile, mfa_token):
    config.read(f'{aws_root_dir}/mfa_arn.conf')
    config.sections()
    mfa_arn = config[profile]['mfa_arn']
    aws_mfa_fetch_command = os.popen(f'aws --profile {profile} sts get-session-token --duration 129600 --serial-number {mfa_arn} --token-code {mfa_token}')
    session_token = aws_mfa_fetch_command.read()
    click.echo(f'The MFA Arn for {profile} is: {mfa_arn}\nTempAccessKey: {session_token}')
    config.read(f'{aws_cred_path}')
    config.sections()
    config[profile]['aws_session_token'] = f'{session_token}'

