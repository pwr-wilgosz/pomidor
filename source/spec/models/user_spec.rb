require 'rails_helper'

RSpec.describe User, type: :model do

  it "should find by access token" do
    user = create :user
    expect(user.access_token).to be_nil
    user.create_api_key
    expect(user.access_token).to be_present
    expect(User.find_by_access_token(user.access_token)).to eq user
    expect(User.find_by_access_token('12345kdj2')).to eq nil
  end
end
