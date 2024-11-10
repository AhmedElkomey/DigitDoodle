from data.dataset_loader import load_data
from models.model_builder import build_model

(x_train, y_train), (x_test, y_test) = load_data()
model = build_model()
model.fit(x_train, y_train, epochs=5)
val_loss, val_acc = model.evaluate(x_test, y_test)
print(f"Validation Loss: {val_loss}, Validation Accuracy: {val_acc}")
model.save('models/digit_recognizer_model.h5')