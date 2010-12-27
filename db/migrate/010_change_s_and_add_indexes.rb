class ChangeSAndAddIndexes < ActiveRecord::Migration
  def self.up
    add_index :rims, :size
    add_index :hubs, :forr
    change_column :hubs, :s, :float, :null => false, :default => "2.5"
  end

  def self.down
    remove_index :rims, :size
    remove_index :hubs, :forr
    change_column :hubs, :s, :float, :null => false, :default => "2.6"
  end
end
