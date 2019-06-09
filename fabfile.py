from fabric import task

PROJECTNAME = 'pizstrip'


@task
def autotest(conn):
    conn.run(('find tests {0} -name "*.py" '
              '| entr -c ./env/bin/pytest --lf -vvv --cov {0}/').format(
             PROJECTNAME), replace_env=False)
