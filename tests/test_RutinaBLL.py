import unittest
from unittest.mock import patch, MagicMock
from BLL.RutinasBLL import (
    crear_rutina_con_ejercicios,
    obtener_listado_rutinas,
    obtener_detalles_rutina_con_ejercicios,
    modificar_rutina_y_ejercicios,
    eliminar_rutina_completa,
    Rutina
)

from BLL.EjercicioBLL import Ejercicio 

class TestRutinaBLL(unittest.TestCase):

    
    def setUp(self):
        self.patcher_rutina_dao = patch('BLL.RutinasBLL.rutina_dao', spec=True)
        self.mock_rutina_dao = self.patcher_rutina_dao.start()
        self.addCleanup(self.patcher_rutina_dao.stop)

        self.patcher_rutina_ejercicio_dao = patch('BLL.RutinasBLL.rutina_ejercicio_dao', spec=True)
        self.mock_rutina_ejercicio_dao = self.patcher_rutina_ejercicio_dao.start()
        self.addCleanup(self.patcher_rutina_ejercicio_dao.stop)
        
        self.mock_rutina_dao.crear_rutina.return_value = 1 
        self.mock_rutina_dao.obtener_todas_las_rutinas.return_value = []
        self.mock_rutina_dao.obtener_rutina_por_id.return_value = None
        self.mock_rutina_dao.actualizar_rutina.return_value = True
        self.mock_rutina_dao.eliminar_rutina.return_value = True

        self.mock_rutina_ejercicio_dao.asociar_ejercicio_a_rutina.return_value = None 
        self.mock_rutina_ejercicio_dao.eliminar_asociaciones_por_rutina.return_value = None
        self.mock_rutina_ejercicio_dao.eliminar_asociaciones_por_ejercicio.return_value = None
        self.mock_rutina_ejercicio_dao.obtener_ejercicios_de_rutina.return_value = []
        
       
        self.patcher_get_ejercicios = patch('BLL.EjercicioBLL.obtener_todos_los_ejercicios')
        self.mock_get_ejercicios = self.patcher_get_ejercicios.start()
        self.mock_get_ejercicios.return_value = [
            Ejercicio(1, "Sentadilla", "Piernas", 10, 3, "Sentadilla con peso corporal"),
            Ejercicio(2, "Press Banca", "Pecho", 8, 4, "Press de banca con barra"),
            Ejercicio(3, "Dominadas", "Espalda", 5, 3, "Dominadas con agarre supino")
        ]
        self.addCleanup(self.patcher_get_ejercicios.stop)

    def test_crear_rutina_con_ejercicios_exito(self):
        nombre = "Rutina Mañana"
        descripcion = "Ejercicios matutinos"
        duracion = "30 minutos"
        ejercicios_ids = [1, 3]

       
        self.mock_rutina_dao.crear_rutina.return_value = 1
        
       
        rutina_completa_mock = Rutina(1, nombre, descripcion, duracion)
        rutina_completa_mock.ejercicios_ids = ejercicios_ids 
        self.mock_rutina_dao.obtener_rutina_por_id.return_value = rutina_completa_mock

        rutina_creada = crear_rutina_con_ejercicios(nombre, descripcion, duracion, ejercicios_ids)

        self.assertIsNotNone(rutina_creada)
        self.assertEqual(rutina_creada.nombre, nombre)
        self.assertEqual(rutina_creada.descripcion, descripcion)
        self.assertEqual(rutina_creada.duracion, duracion)
        self.assertEqual(rutina_creada.ejercicios_ids, ejercicios_ids) 

       
        self.mock_rutina_dao.crear_rutina.assert_called_once()
        self.mock_rutina_dao.obtener_rutina_por_id.assert_called_once_with(1)
        self.mock_rutina_ejercicio_dao.asociar_ejercicio_a_rutina.assert_any_call(1, 1)
        self.mock_rutina_ejercicio_dao.asociar_ejercicio_a_rutina.assert_any_call(1, 3)
        self.assertEqual(self.mock_rutina_ejercicio_dao.asociar_ejercicio_a_rutina.call_count, len(ejercicios_ids))


    def test_crear_rutina_con_ejercicios_nombre_vacio(self):
        nombre = ""
        descripcion = "Descripción"
        duracion = "45 minutos"
        ejercicios_ids = [1]
        
        
        rutina_creada = crear_rutina_con_ejercicios(nombre, descripcion, duracion, ejercicios_ids)

        self.assertIsNone(rutina_creada)
        self.mock_rutina_dao.crear_rutina.assert_not_called()


    def test_crear_rutina_existente_falla(self):
       
        nombre = "Rutina Tarde"
        descripcion = "Ejercicios vespertinos"
        duracion = "60 minutos"
        ejercicios_ids = [2]
        self.mock_rutina_dao.crear_rutina.return_value = None 
        rutina_creada = crear_rutina_con_ejercicios(nombre, descripcion, duracion, ejercicios_ids)

        self.assertIsNone(rutina_creada)
        self.mock_rutina_dao.crear_rutina.assert_called_once()
        self.mock_rutina_dao.obtener_rutina_por_id.assert_not_called() 

    def test_obtener_listado_rutinas_vacio(self):
        self.mock_rutina_dao.obtener_todas_las_rutinas.return_value = []
        rutinas = obtener_listado_rutinas()
        self.assertEqual(rutinas, [])
        self.mock_rutina_dao.obtener_todas_las_rutinas.assert_called_once()

    def test_obtener_listado_rutinas_con_datos(self):
        rutina1 = Rutina(1, "R1", "D1", "30m")
        rutina2 = Rutina(2, "R2", "D2", "45m")
        self.mock_rutina_dao.obtener_todas_las_rutinas.return_value = [rutina1, rutina2]
        rutinas = obtener_listado_rutinas()
        self.assertEqual(len(rutinas), 2)
        self.assertIn(rutina1, rutinas)
        self.assertIn(rutina2, rutinas)
        self.mock_rutina_dao.obtener_todas_las_rutinas.assert_called_once()

    def test_obtener_detalles_rutina_existente(self):
       
        rutina_id = 1
        nombre = "Rutina Test"
        descripcion = "Desc Test"
        duracion = "30min"
        ejercicios_en_rutina_ids = [1, 3]

        rutina_del_dao = Rutina(rutina_id, nombre, descripcion, duracion)
        self.mock_rutina_dao.obtener_rutina_por_id.return_value = rutina_del_dao

        ejercicio1 = Ejercicio(1, "Sentadilla", "Piernas", 10, 3, "Sentadilla con peso corporal")
        ejercicio3 = Ejercicio(3, "Dominadas", "Espalda", 5, 3, "Dominadas con agarre supino")
        self.mock_rutina_ejercicio_dao.obtener_ejercicios_de_rutina.return_value = [ejercicio1, ejercicio3]

   
        detalles = obtener_detalles_rutina_con_ejercicios(rutina_id)

      
        self.assertIsNotNone(detalles)
        self.assertEqual(detalles['rutina'], rutina_del_dao)
        self.assertEqual(len(detalles['ejercicios']), 2)
        self.assertIn(ejercicio1, detalles['ejercicios'])
        self.assertIn(ejercicio3, detalles['ejercicios'])
        
        self.mock_rutina_dao.obtener_rutina_por_id.assert_called_once_with(rutina_id)
        self.mock_rutina_ejercicio_dao.obtener_ejercicios_de_rutina.assert_called_once_with(rutina_id)


    def test_obtener_detalles_rutina_no_existente(self):
    
        self.mock_rutina_dao.obtener_rutina_por_id.return_value = None 


        detalles = obtener_detalles_rutina_con_ejercicios(99)

        self.assertIsNone(detalles)
        self.mock_rutina_dao.obtener_rutina_por_id.assert_called_once_with(99)
        self.mock_rutina_ejercicio_dao.obtener_ejercicios_de_rutina.assert_not_called() 


   
    def test_modificar_rutina_y_ejercicios_exito(self):
        rutina_id = 1
        old_name = "Old Name"
        old_desc = "Old Desc"
        old_duration = "Old Dur"
        old_exercise_ids = [1]

        new_name = "Rutina Editada"
        new_desc = "Nueva descripción"
        new_duration = "40 minutos"
        new_exercise_ids = [1, 2]

      
        self.mock_rutina_dao.obtener_rutina_por_id.return_value = Rutina(rutina_id, old_name, old_desc, old_duration)
       
        self.mock_rutina_dao.actualizar_rutina.return_value = True
       
        self.mock_rutina_ejercicio_dao.obtener_ejercicios_de_rutina.return_value = [
            Ejercicio(1, "Sentadilla", "Piernas", 10, 3, "Sentadilla con peso corporal")
        ]

    
        success = modificar_rutina_y_ejercicios(rutina_id, new_name, new_desc, new_duration, new_exercise_ids)

 
        self.assertTrue(success)
        self.mock_rutina_dao.obtener_rutina_por_id.assert_called_once_with(rutina_id)
        
       
        self.mock_rutina_dao.actualizar_rutina.assert_called_once()
       


        self.mock_rutina_ejercicio_dao.obtener_ejercicios_de_rutina.assert_called_once_with(rutina_id)
        self.mock_rutina_ejercicio_dao.eliminar_asociaciones_por_ejercicio.assert_called_once_with(rutina_id, 1)
        self.mock_rutina_ejercicio_dao.asociar_ejercicio_a_rutina.assert_any_call(rutina_id, 1) 
        self.mock_rutina_ejercicio_dao.asociar_ejercicio_a_rutina.assert_any_call(rutina_id, 2)
        self.assertEqual(self.mock_rutina_ejercicio_dao.asociar_ejercicio_a_rutina.call_count, 2)


    def test_modificar_rutina_y_ejercicios_falla_actualizacion_dal(self):
        rutina_id = 1
        new_name = "Rutina Editada"
        new_desc = "Nueva descripción"
        new_duration = "40 minutos"
        new_exercise_ids = [1, 2]

        self.mock_rutina_dao.obtener_rutina_por_id.return_value = Rutina(rutina_id, "Old Name", "Old Desc", "Old Dur")
        self.mock_rutina_dao.actualizar_rutina.return_value = False 

   
        success = modificar_rutina_y_ejercicios(rutina_id, new_name, new_desc, new_duration, new_exercise_ids)

     
        self.assertFalse(success)
        self.mock_rutina_dao.obtener_rutina_por_id.assert_called_once_with(rutina_id)
        self.mock_rutina_dao.actualizar_rutina.assert_called_once()

        self.mock_rutina_ejercicio_dao.obtener_ejercicios_de_rutina.assert_not_called()
        self.mock_rutina_ejercicio_dao.eliminar_asociaciones_por_ejercicio.assert_not_called()
        self.mock_rutina_ejercicio_dao.asociar_ejercicio_a_rutina.assert_not_called()


    def test_modificar_rutina_y_ejercicios_rutina_no_existe(self):
        rutina_id = 99 
        new_name = "Rutina Editada"
        new_desc = "Nueva descripción"
        new_duration = "40 minutos"
        new_exercise_ids = [1, 2]

        self.mock_rutina_dao.obtener_rutina_por_id.return_value = None 

    
        success = modificar_rutina_y_ejercicios(rutina_id, new_name, new_desc, new_duration, new_exercise_ids)

  
        self.assertFalse(success)
        self.mock_rutina_dao.obtener_rutina_por_id.assert_called_once_with(rutina_id)
        self.mock_rutina_dao.actualizar_rutina.assert_not_called()
        self.mock_rutina_ejercicio_dao.obtener_ejercicios_de_rutina.assert_not_called()
        self.mock_rutina_ejercicio_dao.eliminar_asociaciones_por_ejercicio.assert_not_called()
        self.mock_rutina_ejercicio_dao.asociar_ejercicio_a_rutina.assert_not_called()

 
    def test_eliminar_rutina_completa_exito(self):
   
        rutina_id = 1
        self.mock_rutina_dao.eliminar_rutina.return_value = True

     
        success = eliminar_rutina_completa(rutina_id)

        self.assertTrue(success)
        self.mock_rutina_ejercicio_dao.eliminar_asociaciones_por_rutina.assert_called_once_with(rutina_id)
        self.mock_rutina_dao.eliminar_rutina.assert_called_once_with(rutina_id)

    def test_eliminar_rutina_completa_falla_no_existe(self):
    
        rutina_id = 99
        self.mock_rutina_dao.eliminar_rutina.return_value = False

      
        success = eliminar_rutina_completa(rutina_id)

        self.assertFalse(success)
       
        self.mock_rutina_ejercicio_dao.eliminar_asociaciones_por_rutina.assert_called_once_with(rutina_id)
        self.mock_rutina_dao.eliminar_rutina.assert_called_once_with(rutina_id)

if __name__ == '__main__':
    unittest.main()