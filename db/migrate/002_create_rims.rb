class CreateRims < ActiveRecord::Migration
  def self.up
    create_table :rims, :options => 'engine=MyISAM' do |t|
      # t.column :name, :string
      t.column :description, :string
      t.column :erd, :float,:null => false, :default => 0
      t.column :osb, :float,:null => false, :default => 0
      t.column :size, :string
      t.column :iso, :string
    end
  end

  def self.down
    drop_table :rims
  end
end
