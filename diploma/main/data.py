class Building_and_Condition_Types:

    def get_building_type(index):

        building_types = {
            0: 'other', 
            1: 'brick',
            2: 'wooden',
            3: 'panel',
            4: 'monolithic'
        }

        return building_types[index]


    def get_condition_type(index):
        
        condition_types = {
            0: 'not completed', 
            1: 'open plan', 
            2: 'average', 
            3: 'rough finish', 
            4: 'good', 
            5: 'needs renovation'
        }

        return condition_types[index]