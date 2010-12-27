require File.dirname(__FILE__) + '/../test_helper'

class RimTest < Test::Unit::TestCase
  fixtures :rims

  def setup
    @front = Rim.find(1)
    @rear = Rim.find(2)
  end

  def test_create
    assert_kind_of Rim, @front
    assert_kind_of Rim, @rear
  end
end
