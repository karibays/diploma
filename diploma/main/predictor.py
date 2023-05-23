import numpy as np
import tensorflow as tf


class myModel:
    model = tf.keras.models.load_model(r'C:\Users\karib\Desktop\diploma\models\model_v2')

    def scale_data(self, data):
        means = np.array([6.68714563e+02, 2.00598526e+00, 9.23103213e-01, 2.42481203e+00,
        3.46777119e+00, 6.44907724e-01, 3.63636364e-01, 2.50512645e-01,
        4.13192071e-01, 4.03964457e-01, 8.20232399e-02])

        vars = np.array([2.67955554e+05, 7.00102538e-01, 1.58499597e+00, 4.78296604e+00,
        4.97651762e-01, 2.29001752e-01, 2.31404959e-01, 1.87756060e-01,
        2.43147910e-01, 2.40777174e-01, 7.52954280e-02])
        
        return (data - means) / (vars ** 0.5)
    
    
    def predict(self, total_area, number_of_levels, buildingType, condition, ceilings,
                parking, firealarm, security, video_surveillance, alarm_system, optics):
        
        parking = int(parking == True)
        firealarm = int(firealarm == True)
        security = int(security == True)
        video_surveillance = int(video_surveillance == True)
        alarm_system = int(alarm_system == True)
        optics = int(optics == True)

        data_to_predict = np.array([total_area, number_of_levels, buildingType, condition,
                                    ceilings, parking, firealarm, security, video_surveillance,
                                    alarm_system, optics]).astype(float)
        
        data = self.scale_data(self, data_to_predict)
        data = np.expand_dims(data, 0)

        prediction = self.model.predict(data)[0][0]
        prediction = tf.math.exp(prediction).numpy()
        prediction = prediction - prediction % 10000

        return prediction
