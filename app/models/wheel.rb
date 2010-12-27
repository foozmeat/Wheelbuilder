class Wheel
  attr_accessor :rim, :hub, :spokes, :cross, :nipple_correction

  def initialize
    @hub = Hub.new
    @rim = Rim.new
    @cross = 3
    @spokes = 32
    @nipple_correction = 0
  end

  def wl_effective
    @hub.wl.to_f - @rim.osb.to_f
  end

  def wr_effective
    @hub.wr.to_f + @rim.osb.to_f
  end
  
  def l_length

    return 0 unless (@spokes != nil and  @hub.dl != 0 and @rim.erd != 0 and @cross != nil)

    result = Math.sqrt( 
      ( (@hub.dl / 2 * Math.sin(2 * Math::PI * @cross / (@spokes / 2))) ** 2) +
      ( (@rim.erd / 2 - ( ( @hub.dl / 2) * Math.cos( 2 * Math::PI * @cross / ( @spokes / 2)))) ** 2) +
      ( wl_effective ** 2)
    ) - (@hub.s / 2) - @nipple_correction
    
    sprintf("%.1f", result)
  end

  def r_length

    return 0 unless (@spokes != nil and  @hub.dr != 0 and @rim.erd != 0 and @cross != nil)

    result = Math.sqrt( 
      ( (@hub.dr / 2 * Math.sin(2 * Math::PI * @cross / (@spokes / 2))) ** 2) +
      ( (@rim.erd / 2 - ( ( @hub.dr / 2) * Math.cos( 2 * Math::PI * @cross / ( @spokes / 2)))) ** 2) +
      ( wr_effective ** 2)
    ) - (@hub.s / 2) - @nipple_correction
    
    sprintf("%.1f", result)
  end
  
  def patterns
    Hash[
      0 => "0-cross (Radial)",
      1 => "1-cross",
      2 => "2-cross",
      3 => "3-cross",
      4 => "4-cross",
      5 => "5-cross",
      ]
  end
  
  def nipple_corrections
    Hash[
      0 => "12mm",
      1 => "14mm",
      3 => "16mm"
      ]
  end
  
  def pattern_for_cross
    self.patterns[self.cross]
  end

  def nipple_length_for_correction
    self.nipple_corrections[self.nipple_correction]
  end
  
  def spoke_counts
    Array[16, 20, 24, 28, 32, 36, 40, 48]
  end
end