Biblib port
===========

## 1. mongodb

		$ cd ~/Sites/reference_manager
		$ cd mongodb
		$ mongodb --path .

## 2. edit config.json and init forccast

	$ cd ~/Sites/reference_manager
	$ vi conf/config.json
			…
			
			[change mongodb.default_corpus to aime or forccast]
			…
	$ workon remanager
	$ python biblib init --help
	$ python biblib init -c forccast
		

## 3. start twisted !


	$ cd ~/Sites/reference_manager
	$ workon remanager
	$ twistd -noy biblib/services/jsonrpc_service.tac -l -

	$ cd ~/Sites/reference_manager/biblib/front/
	$ python -m SimpleHTTPServer 8090

that's all folks !