# Test the shape renderer module
import os
import sys
import unittest

from generate_universe_lib_test.test_results_comparitor.compare import TestResultComparator

# access the main library
sys.path.append(os.path.abspath(os.path.join(__file__,
                                "../../../../main/python")))

# access the test library
sys.path.append(os.path.abspath(os.path.join(__file__,
                                "../../../../test/python")))

from generate_universe_lib.pygame_windows.shape_renderer import ShapeDraw


class ShapeRendererTest(unittest.TestCase):
    def setUp(self):
        self.shape_draw = ShapeDraw()

    def generate_image_file_name(self):
        # Get the name of the current module
        module_path = os.path.join(__file__, '../'+__name__.split(".")[-1])

        # Replace dots with slashes to create a relative file path
        module_path = os.path.abspath(module_path)

        # Append the test name and '.png' to the end of the file path
        file_name = self._testMethodName + '.png'

        # Make the path relative to the test python folder
        file_name = os.path.join(module_path+'_test_results', file_name)

        return file_name

    # Test the initialization of the sphere
    def test_initialize_sphere(self):
        self.shape_draw.initialize_sphere(10, 10)
        self.assertEqual(92, len(self.shape_draw.vertices))
        self.assertEqual(201, len(self.shape_draw.edges))

    # Test the initialization of the sphere
    def test_initialize_sphere_detailed(self):
        self.shape_draw.initialize_sphere(24, 12)
        self.assertEqual(266, len(self.shape_draw.vertices))
        self.assertEqual(577, len(self.shape_draw.edges))

    def test_initialize_sphere_image(self):
        self.shape_draw.initialize_sphere(24, 12)
        with TestResultComparator(self.generate_image_file_name()) as compare:
            compare.compare_or_save_image(self.shape_draw.render_as_image_file())

    def test_initialize_cube_image(self):
        self.shape_draw.initialize_cube()
        with TestResultComparator(self.generate_image_file_name()) as compare:
            compare.compare_or_save_image(self.shape_draw.render_as_image_file())

    def test_initialize_2d_star_image(self):
        self.shape_draw.initialize_2d_star(5)
        with TestResultComparator(self.generate_image_file_name()) as compare:
            compare.compare_or_save_image(self.shape_draw.render_as_image_file())

    def test_initialize_3d_star_image(self):
        self.shape_draw.initialize_3d_star(25, 13, 0.75)
        with TestResultComparator(self.generate_image_file_name()) as compare:
            compare.compare_or_save_image(self.shape_draw.render_as_image_file())

    def test_initialize_pyramid_image(self):
        self.shape_draw.initialize_pyramid()
        with TestResultComparator(self.generate_image_file_name()) as compare:
            compare.compare_or_save_image(self.shape_draw.render_as_image_file())

    def test_initialize_none_image(self):
        self.shape_draw.initialize_none()
        with TestResultComparator(self.generate_image_file_name()) as compare:
            compare.compare_or_save_image(self.shape_draw.render_as_image_file())

# Run the tests
if __name__ == '__main__':
    unittest.main()
