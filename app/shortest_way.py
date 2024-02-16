from collections import deque

def bfs(field:list, start:list, end:list) -> list:
    if start and end:
        # Инициализация массивов и очереди
        INF:int = 10**9
        len_x:int = len(field[0][0])
        len_y:int = len(field[0])
        len_z:int = len(field)

        distance:list = [[[INF]*len_x for _ in range(len_y)] for _ in range(len_z)]
        come_from:list = [[[None]*len_x for _ in range(len_y)] for _ in range(len_z)]
        visited:list = [[[False]*len_x for _ in range(len_y)] for _ in range(len_z)]
        neighbors:list = [(0,0,1),(0,0,-1),(0,1,0),(0,-1,0),(1,0,0),(-1,0,0)]

        queue:deque = deque() 

        # Задания значений для начальной точки
        distance[start[0]][start[1]][start[2]] = 0
        visited[start[0]][start[1]][start[2]] = True
        queue.append(start)
        
        # Основная логика
        while len(queue)!=0:
            z,x,y = queue.popleft()
            for dx,dy,dz in neighbors:
                nx, ny, nz = x + dx, y + dy, z + dz
                if 0 < nx < len_y and 0 < ny < len_x and 0 < nz < len_z and not visited[nz][nx][ny] and field[nz][nx][ny]!= '#':
                    distance[nz][nx][ny] = distance[z][x][y]+1
                    come_from[nz][nx][ny] = (z,x,y)
                    visited[nz][nx][ny] = True
                    queue.append((nz,nx,ny))
    
        cur:list = end
        path:list = []
        while cur is not None:
            path.append(cur)
            cur = come_from[cur[0]][cur[1]][cur[2]]
        path.reverse()
        return path[1:-1]
    else:
        return []