################# WORKFLOW ############################################

run_preprocess:
	python -c 'from taxifare.interface.main import preprocess; preprocess()'

run_train:
	python -c 'from taxifare.interface.main import train; train()'

run_pred:
	python -c 'from taxifare.interface.main import pred; pred()'

run_evaluate:
	python -c 'from taxifare.interface.main import evaluate; evaluate()'

run_all: run_preprocess run_train run_pred run_evaluate

################# TESTS ################################################

default: pylint pytest

pylint:
    find . -iname "*.py" -not -path "./tests/*" | xargs -n1 -I {}  pylint --output-format=colorized {}; true

pytest:
    PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes


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
