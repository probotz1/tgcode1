async def AddUserToDatabase(bot, event):
    user_id = event.from_user.id
    # Code to add user to the database
    await db.add_user(user_id)
