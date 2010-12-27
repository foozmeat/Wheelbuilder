class MRU
  
  @max_length = 10
  
  def initialize
    @list = Array.new
  end
  
  def add(item)
    
    
    
    if @list.length > @max_length
      @list.pop
    end
    
    @list.unshift(item)
    self
  end
  
end