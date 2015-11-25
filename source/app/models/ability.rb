class Ability
  include CanCan::Ability

  def initialize(user)
    if user.present?
      can :manage, List, user_id: user.id
      can :manage, Task, list: { user_id: user.id }
    end

  end
end
