class RemoveWidthAndWeight < ActiveRecord::Migration
  def self.up
    remove_column :rims, :weight
    remove_column :rims, :width
    
    remove_column :hubs, :weight
  end

  def self.down
    add_column :rims, :weight, :float, :null => true
    add_column :rims, :width, :int, :null => true

    add_column :hubs, :weight, :float, :null => true
  end
end
