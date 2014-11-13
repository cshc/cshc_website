@echo off
REM To be run from the cshc_website directory
REM GraphVis must be installed first
echo Generating graphical representations of all apps
mkdir ..\model_visualization
python cshcsite\manage.py graph_models awards -o ..\model_visualization\awards_models.png
python cshcsite\manage.py graph_models competitions -o ..\model_visualization\competitions_models.png
python cshcsite\manage.py graph_models core -o ..\model_visualization\core_models.png
python cshcsite\manage.py graph_models matches -o ..\model_visualization\matches_models.png
python cshcsite\manage.py graph_models members -o ..\model_visualization\members_models.png
python cshcsite\manage.py graph_models opposition -o ..\model_visualization\opposition_models.png
python cshcsite\manage.py graph_models teams -o ..\model_visualization\teams_models.png
python cshcsite\manage.py graph_models training -o ..\model_visualization\training_models.png
python cshcsite\manage.py graph_models venues -o ..\model_visualization\venues_models.png

