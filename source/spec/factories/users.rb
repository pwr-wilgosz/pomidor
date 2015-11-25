FactoryGirl.define do
  factory :user do
    sequence(:email) { |k| "email#{k}@example.com" }
    password 'password'
    password_confirmation 'password'
  end
end
