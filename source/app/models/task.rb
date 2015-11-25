class Task < ActiveRecord::Base
  belongs_to :list

  include WithIdentifier

  PRIORITIES = (1..4).to_a
  QUARTER_SIZE = { x: 500, y: 500 }

  QUARTER_1 = {
                x: { min: 1, max: QUARTER_SIZE[:x] },
                y: { min: 1, max: QUARTER_SIZE[:y] }
              }
  QUARTER_2 = {
                x: { min: QUARTER_SIZE[:x]+1, max: 2*QUARTER_SIZE[:x] },
                y: { min: 1, max: QUARTER_SIZE[:y] }
              }
  QUARTER_3 = {
                x: { min: 1, max: QUARTER_SIZE[:x] },
                y: { min: QUARTER_SIZE[:x]+1, max: 2*QUARTER_SIZE[:y] }
              }
  QUARTER_4 = {
                x: { min: QUARTER_SIZE[:x]+1, max: 2*QUARTER_SIZE[:x] },
                y: { min: QUARTER_SIZE[:y]+1, max: 2*QUARTER_SIZE[:y] }
              }

  scope :quarter1, ->{ where(priority: 1) }
  scope :quarter2, ->{ where(priority: 2) }
  scope :quarter3, ->{ where(priority: 3) }
  scope :quarter4, ->{ where(priority: 4) }


  after_initialize :set_position
  AVAILABLE_LABELS = ["Default", "Primary", "Success", "Info", "Warning", "Danger"]

  def self.random_label
    AVAILABLE_LABELS[rand(AVAILABLE_LABELS.length)].downcase
  end

  private

  def set_position
    self.priority ||= rand(4)+1
    self.x ||= rand(QUARTER_SIZE[:x])
    self.y ||= rand(QUARTER_SIZE[:y])
  end
end
