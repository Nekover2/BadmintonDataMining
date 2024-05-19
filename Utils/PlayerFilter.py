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
    if(len(courtCoords) < 4):
        return playerCoords
    filteredPlayers = []
    for player_coordinate in playerCoords:
        #maybe if the player is jumping, we should consider the highest jump
        if(courtCoords[0][0] <= player_coordinate[2] <= courtCoords[2][0]
           and courtCoords[1][1] - highest_jump<= player_coordinate[3] <= courtCoords[0][1] + highest_jump):
            filteredPlayers.append(player_coordinate)

    return filteredPlayers