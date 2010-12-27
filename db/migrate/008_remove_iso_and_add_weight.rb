class RemoveIsoAndAddWeight < ActiveRecord::Migration
  def self.up
    remove_column :rims, :iso
    
    add_column :rims, :weight, :float, :null => true
    add_column :hubs, :weight, :float, :null => true
    
    change_column :rims, :size, :integer, :null => false, :default => 0
    change_column :rims, :width, :integer, :null => true, :default => nil
    change_column :hubs, :description, :string, :null => false, :default => ""
    change_column :rims, :description, :string, :null => false, :default => ""
    change_column :hubs, :forr, :string, :null => false, :default => "f"
    change_column :hubs, :s, :float, :null => false, :default => "2.6"
  end

  def self.down
    add_column :rims, :iso, :string
    
    remove_column :rims, :weight
    remove_column :hubs, :weight
    
    change_column :rims, :size, :string
    change_column :rims, :width, :integer
    change_column :hubs, :description, :string, :null => true
    change_column :rims, :description, :string, :null => true
    change_column :hubs, :forr, :string, :null => true
    change_column :hubs, :s, :float, :null => false, :default => "0"
  end
end
