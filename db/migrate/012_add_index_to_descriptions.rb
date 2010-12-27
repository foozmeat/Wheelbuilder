class AddIndexToDescriptions < ActiveRecord::Migration
  def self.up
    
    remove_index :rims, :description
    remove_index :hubs, :description

    add_index :rims, :description
    add_index :hubs, :description
  end

  def self.down
    remove_index :rims, :description
    remove_index :hubs, :description
    
    add_index :rims, :description, "FULLTEXT"
    add_index :hubs, :description, "FULLTEXT"
    
  end
end
