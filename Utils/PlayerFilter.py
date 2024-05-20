def filter_players(playerCoords, courtCoords, highest_jump = 30 ):
    # playerCoords: 2D list of player coordinates
    # courtCoords: 2D list of court coordinates
    # return: 2D list of player coordinates

    # Filter out players that are not on the court
    filteredPlayers = []
    for player_coordinate in playerCoords:
        #maybe if the player is jumping, we should consider the highest jump
        if(courtCoords[0] <= player_coordinate[2] <= courtCoords[2]
           and courtCoords[1] + highest_jump<= player_coordinate[3] <= courtCoords[3]+highest_jump):
            filteredPlayers.append(player_coordinate)

    return filteredPlayers

def filter_players_by_corner(playerCoords, courtCoords, highest_jump = 30 ):
    # playerCoords: 2D list of player coordinates
    # courtCoords: 2D list of court coordinates
    # return: 2D list of player coordinates

    # Filter out players that are not on the court
    
    #extract 4 important value...
    if(len(courtCoords) < 4):
        return playerCoords
    min_x = 9999
    min_y = 9999
    max_x = 0
    max_y = 0
    
    for corner in courtCoords:
        if corner[0] > max_x : max_x = corner[0]
        if corner[1] > max_y : max_y = corner[1]
        if corner[0] < min_x : min_x = corner[0]
        if corner[1] < min_y : min_y = corner[1]
    filteredPlayers = []
    print(min_x, max_x, min_y, max_y)
    for player_coordinate in playerCoords:
        print(player_coordinate[2], player_coordinate[3])
        #maybe if the player is jumping, we should consider the highest jump
        if(min_x <= player_coordinate[2] <= max_x):
            if(min_y - highest_jump <= player_coordinate[3] <= max_y + highest_jump):
                filteredPlayers.append(player_coordinate)
    print(filteredPlayers)
    return filteredPlayers