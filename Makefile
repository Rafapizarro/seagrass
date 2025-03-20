.DEFAULT_GOAL := default
################# WORKFLOW ############################################

run_preprocess:
	python -c 'from seagrass.interface.main import preprocess; preprocess(max_distance=0.01)'

run_train:
	python -c 'from seagrass.interface.main import train; train(max_distance=0.01)'

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
