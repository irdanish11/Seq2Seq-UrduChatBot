call C:\Users\%USERNAME%\Anaconda3\Scripts\activate.bat C:\Users\%USERNAME%\Anaconda3
start http://127.0.0.1:5000
python app.py "models\cornell_movie_dialog\trained_model_v2\best_weights_training.ckpt"


cmd /k