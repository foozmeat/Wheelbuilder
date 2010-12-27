class CreateHubs < ActiveRecord::Migration
  def self.up
    create_table :hubs, :options => 'engine=MyISAM' do |t|
      # t.column :name, :string
      t.column :description, :string
      t.column :s, :float,:null => false, :default => 0
      t.column :dl, :float,:null => false, :default => 0
      t.column :dr, :float,:null => false, :default => 0
      t.column :wl, :float,:null => false, :default => 0
      t.column :wr, :float,:null => false, :default => 0
      t.column :old, :float,:null => false, :default => 0
      t.column :cogs, :string
      t.column :forr, :string
      
    end
  end

  def self.down
    drop_table :hubs
  end
end
