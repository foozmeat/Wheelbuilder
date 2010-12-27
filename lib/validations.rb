module Validations
  
  def validate_greater_than_zero(*attributes)
    error_message = 'must be greater than zero'
    attributes.each do |attribute|
      self.errors.add(attribute, error_message) unless valid_greater_than_zero?(self.send(attribute))
    end
    
  end
  
  
  def valid_greater_than_zero?(number)
    return true if number.to_f > 0 or number.eql?("") or number.nil?
  end
end

class ActiveRecord::Base
  include Validations
end
