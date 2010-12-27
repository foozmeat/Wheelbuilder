class Rim < ActiveRecord::Base

  validates_presence_of :description, :erd, :osb, :size
  validates_uniqueness_of :description, :scope => :size
  validates_numericality_of :erd, :osb, :size, :allow_nil => true
  validates_as_email_address :email, :on => :create

  def self.search(search, size, page)
    
    c_strings = []
    conditions = []

    if !search.nil? and !search.eql?("")
      c_strings << "description like ?"
      conditions << "%#{search}%"
    end

    if !size.nil? and !size.eql?("")
      c_strings << "size = ?"
      conditions << size
    end
    
    conditions.unshift(c_strings.join(" and ")) if !c_strings.empty?

    if conditions.empty?
      paginate :per_page => 25, :page => page, :order => 'description'
    else
      paginate :per_page => 25, :page => page, :conditions => conditions, :order => 'description'
    end
    
  end

  def size_for_display
    
    result = ""
    
    sizes.each{|s|
      s.each {|key, value|
        result = value if self.size == key
      }
    }
    
    result
  end

  def description_for_menu
    "#{self.description} (#{self.size_for_display})"
    
  end
  
  
  def rim_correction_factor
    
    rc = { 
      # 622 => 315, 
      # 559 => 292, #interpolated
      # 584 => 304, #interpolated
      # 630 => 325, 
      # 571 => 300,
      # 520 => 274, #interpolated
      # 507 => 270,
      # 451 => 242, #interpolated
      # 406 => 225,
      # 355 => 200,
      # 349 => 194, #interpolated
      # 305 => 175,
      
      0 => 0,
      635 => 317,
      630 => 315,
      622 => 315,
      584 => 301,
      571 => 295,
      559 => 300,
      520 => 274,
      507 => 270,
      451 => 245,
      406 => 225,
      355 => 204,
      349 => 200,
      305 => 183
      
    }
    
    radius = self.erd / 2
    rcf = radius - rc[self.size]
    rcf.round
    
  end

  def sizes
    Array[
      { 622 => '700C' },
#      { 559 => '26" x 1.00-2.125' },
      { 559 => '26"' },
#      { 584 => '650B &mdash; 26" x 1 1/2' },
      { 584 => '650B' },
      { 630 => '27"' },
      { 635 => '28"' },
#      { 571 => '650C &mdash; 26" x 1 &mdash; 26" x 1 3/4' },
      { 571 => '650C' },
#      { 520 => '24" x 1 &mdash; 24" x 1 1/8' },
      { 520 => '24"' },
#      { 507 => '24" x 1.5-2.125' },
      { 507 => '24"' },
#      { 451 => '20" x 1 1/8 &mdash; 26" x 1 1/4 &mdash; 26" x 1 3/8' },
      { 451 => '20"' },
#      { 406 => '20" x 1.5-2.125' },
      { 406 => '20"' },
#      { 349 => '16" x 1 3/8' },
      { 349 => '16"' },
#      { 305 => '16" x 1.75-2.125' },
      { 305 => '16"' },
      ]
  end

  protected
    def validate
      validate_greater_than_zero('erd', 'size')
    end

end
