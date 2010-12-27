class Hub < ActiveRecord::Base

  validates_presence_of :description, :s, :dl, :dr, :wl, :wr, :old, :forr
  validates_uniqueness_of :description, :scope => :forr
  validates_numericality_of :s, :dl, :dr, :wl, :wr, :old, :allow_nil => true
  validates_as_email_address :email, :on => :create
  
  def self.search(search, forr, page)

    c_strings = []
    conditions = []

    if !search.nil? and !search.eql?("")
      c_strings << "description like ?"
      conditions << "%#{search}%"
    end

    if !forr.nil? and !forr.eql?("")
      c_strings << "forr = ?"
      conditions << forr
    end

    conditions.unshift(c_strings.join(" and ")) if !c_strings.empty?
    
    if conditions.empty?
      paginate :per_page => 25, :page => page, :order => 'description'
    else
      paginate :per_page => 25, :page => page, :conditions => conditions, :order => 'description'
    end
  end

  def a
    (@attributes['old'].to_f / 2) - @attributes['wl'].to_f
  end

  def b
    (@attributes['old'].to_f / 2) - @attributes['wr'].to_f
  end

  def forr_for_display
    if self.forr.eql?("F")
      "Front"
    else
      "Rear"
    end
  end

  def description_for_menu
    "#{self.description} (#{self.forr_for_display})"
  end

protected
  def validate
    validate_greater_than_zero('s', 'dl', 'dr', 'wl', 'wr', 'old')
  end

end
