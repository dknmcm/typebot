from src.core.region_selector import RegionSelector


def test_callback(x, y, width, height):
    """Test callback to see if coordinates are captured correctly"""
    print(f"Selected region: x={x}, y={y}, width={width}, height={height}")
    print("Region selector working correctly!")


if __name__ == "__main__":
    selector = RegionSelector(test_callback)
    selector.show_selector()
