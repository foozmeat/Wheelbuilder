class AddDescriptionIndexes < ActiveRecord::Migration
  def self.up
    add_index :rims, :description, "FULLTEXT"
    add_index :hubs, :description, "FULLTEXT"
  end

  def self.down
    remove_index :rims, :description
    remove_index :hubs, :description
  end
end
