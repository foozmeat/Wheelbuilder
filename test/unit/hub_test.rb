require File.dirname(__FILE__) + '/../test_helper'

class HubTest < Test::Unit::TestCase
  fixtures :hubs

  def setup
    @front = Hub.find(1)
    @rear = Hub.find(2)
  end

  def test_create
    assert_kind_of Hub, @front
    assert_kind_of Hub, @rear
  end
  
  def test_front_a
    assert_equal 13.8.to_s, @front.a.to_s
  end

  def test_rear_a
    assert_equal 24.3.to_s, @rear.a.to_s
  end

  def test_front_b
    assert_equal 13.8.to_s, @front.b.to_s
  end

  def test_rear_b
    assert_equal 48.0.to_s, @rear.b.to_s
  end
end
