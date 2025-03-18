.DEFAULT_GOAL := default
################# WORKFLOW ############################################

run_preprocess:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
	python -c 'from seagrass.interface.main import preprocess; preprocess(max_distance=0.01, limit=100000)'

run_train:
	python -c 'from seagrass.interface.main import train; train(max_distance=0.01, limit=100000)'
=======
	python -c 'from seagrass.interface.main import preprocess; preprocess(max_distance=0.01, limit=1000)'

run_train:
	python -c 'from seagrass.interface.main import train; train(max_distance=0.01, limit=1000)'
>>>>>>> 18dbd0ae0e921d8370ea73d4380007ece1d3e54b
=======
	python -c 'from seagrass.interface.main import preprocess; preprocess(max_distance=0.01, limit=1000)'

run_train:
	python -c 'from seagrass.interface.main import train; train(max_distance=0.01, limit=1000)'
>>>>>>> 18dbd0ae0e921d8370ea73d4380007ece1d3e54b
=======
	python -c 'from seagrass.interface.main import preprocess; preprocess(max_distance=0.01, limit=100000)'

run_train:
	python -c 'from seagrass.interface.main import train; train(max_distance=0.01, limit=100000)'
>>>>>>> d04b5d7b2ebf61935a50d57d94b9dcacc17ac328

run_pred:
	python -c 'from seagrass.interface.main import pred; pred()'

run_evaluate:
	python -c 'from seagrass.interface.main import evaluate; evaluate()'

run_all: run_preprocess run_train run_pred run_evaluate


################# LOCAL FILES ################################################

ML_DIR=~/.seagrass/mlops

reset_local_files:
	rm -rf ${ML_DIR}
	mkdir -p ~/.seagrass/mlops/data/
	mkdir ~/.seagrass/mlops/data/raw
	mkdir ~/.seagrass/mlops/data/processed
	mkdir ~/.seagrass/mlops/training_outputs
	mkdir ~/.seagrass/mlops/training_outputs/metrics
	mkdir ~/.seagrass/mlops/training_outputs/models
	mkdir ~/.seagrass/mlops/training_outputs/params

################# TESTS ################################################

# default: pylint pytest

# pylint:
#     find . -iname "*.py" -not -path "./tests/*" | xargs -n1 -I {}  pylint --output-format=colorized {}; true

# pytest:
#     PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes
