if [ $# -eq 1 ] ; then
    if [ "$1" = "local" ] ; then
        python manage.py runserver --settings=_config.settings.base-dev
    elif [ "$1" = "distrib" ] ; then
        sudo python manage.py runserver --settings=_config.settings.base-dist 0:80
    else
        echo "Incorrect argument : $1"
    fi
else
    echo "Incorrect number of arguments : 1 needed but $# given"
fi