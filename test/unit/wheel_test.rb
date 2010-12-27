require File.dirname(__FILE__) + '/../test_helper'

class WheelTest < Test::Unit::TestCase
  fixtures :rims
  fixtures :hubs
  
  def setup
    @front_hub = Hub.find(1)
    @rear_hub = Hub.find(2)

    @front_rim = Rim.find(1)
    @rear_rim = Rim.find(2)

    @front_wheel = Wheel.new
    @front_wheel.hub = @front_hub
    @front_wheel.rim = @front_rim
    @front_wheel.spokes = 36
    
    @rear_wheel = Wheel.new
    @rear_wheel.hub = @rear_hub
    @rear_wheel.rim = @rear_rim
    @rear_wheel.spokes = 36

  end

  def test_create
    assert_kind_of Hub, @front_wheel.hub
    assert_kind_of Hub, @rear_wheel.hub
    assert_kind_of Rim, @front_wheel.rim
    assert_kind_of Rim, @rear_wheel.rim
  end

  def test_front_wl_effective
    assert_equal 36.2.to_f, @front_wheel.wl_effective
    
  end

  def test_front_wr_effective
    assert_equal 36.2.to_f, @front_wheel.wr_effective
  
  end

  def test_rear_wl_effective
    assert_equal 36.7.to_f, @rear_wheel.wl_effective
    
  end

  def test_rear_wr_effective
    assert_equal 21.0.to_f, @rear_wheel.wr_effective
  
  end

#  def test_print
#    print "Hub dL" + @front_wheel.hub['dl'] + "\n"
#  end

  def test_front_l_length
    assert_equal 293.8.to_s, @front_wheel.l_length(3)
  end

  def test_front_r_length
    assert_equal 293.8.to_s, @front_wheel.r_length(3)
  end

  def test_rear_l_length
    assert_equal 290.0.to_s, @rear_wheel.l_length(3)
  end

  def test_rear_r_length
    assert_equal 288.4.to_s, @rear_wheel.r_length(3)
  end


end
