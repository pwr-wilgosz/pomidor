class AddIdentifierToTaskAndList < ActiveRecord::Migration
  def change
    add_column :lists, :identifier, :string
    add_column :tasks, :identifier, :string
  end
end
