virtualenv env/
chmod +x env/bin/activate
echo pwd | read path_full
source $path_full"./env/bin/activate"
/bin/bash -c ". env/bin/activate; exec /bin/bash -i"
