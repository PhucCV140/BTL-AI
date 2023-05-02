# Sử dụng hàm deepcopy của module copy, giúp tạo bản sao mới của một đối tượng
from copy import deepcopy

TIME_OUT = 300

# Triển khai hàm support
# Bộ lưu trữ trạng thái mỗi bước

class state:  # Tạo lớp state giúp định nghĩa một trạng thái của trò chơi Sokoban
    # Hàm khởi tạo chứa các thông tin sau
    # board lưu ma trận bản đồ với level được chọn
    # state_parent là trạng thái cha của trạng thái hiện tại (có thể có hoặc không)
    # list_check_point lưu ma các điểm cần kiểm tra đối với ma trận bản đồ
    def __init__(self, board, state_parent, list_check_point):
        self.board = board # Lưu trữ ma trận bản đồ của trò chơi hiện tại
        self.state_parent = state_parent # Lưu trữ trạng thái cha của trạng thái hiện tại
        self.cost = 1 # Lưu trữ giá trị của trạng thái hiện tại
        self.heuristic = 0 # Lưu trữ giá trị hàm heuristic của trạng thái hiện tại (khởi tạo bằng 0) 
        self.check_points = deepcopy(list_check_point) # Tạo bản sảo của list_check_point lưu vào check_point tránh gay ảnh hưởng đến đối tượng gốc khi thực hiện thay đổi
    
    # Hàm đệ quy trả về các ma trận bản đồ từ trạng thái ban đầu đến trạng thái hiện tại 
    def get_line(self): # Sử dụng vòng lặp để tìm bảng danh sách từ đầu đến trạng thái này
        if self.state_parent is None: # Nếu như state_parent hiện tại là None, tức là đang ở trạng thí ban đầu của trò chơi (không  có trạng thái cha)
            return [self.board] # Thì trả về danh sách của ma trận bản đồ hiện tại 
        return (self.state_parent).get_line() + [self.board] # Trả về danh sách chưa tất cả các trạng thái đầu tiên đến trạng thái hiện tại 

    # Tính toán hàm heuristic được sử dụng cho thuật toán A*
    def compute_heuristic(self):
        list_boxes = find_boxes_position(self.board) # Lấy danh sách tọa độ các hộp từ hàm find_boxes_position bên dưới
        if self.heuristic == 0: # Nếu như hàm heuristic chưa được tính toán trước đó thì sẽ thực hiện tính toán
            # Giá trị heuristic được tính bằng tổng chi phí và khoảng cách từ ô đó đến điểm đích 
            self.heuristic = self.cost + abs(sum(list_boxes[i][0] + list_boxes[i][1] - self.check_points[i][0] - self.check_points[i][1] for i in range(len(list_boxes))))
        return self.heuristic # Nếu như đã dược tính toán thì trả về giá trị hueristic mà không cần tính lại
    
    # 2 hàm dưới đây được sử dụng để sắp xếp các trạng thái trong hàng đợi ưu tiên theo giá trị heuristic tăng dần
    # Giúp cho thuật toán A* và BFS hoạt động hiệu quả hơn
    def __gt__(self, other): # Sử dụng để so sánh giá trị của hàm heuristic 
        if self.compute_heuristic() > other.compute_heuristic(): # Nếu giá trị heuristic hiện tại lớn hơn giá trị heuristic khác thì trả về True
            return True
        else: # Ngươc lại sẽ trả về False
            return False
    def __lt__(self, other): # Sử dụng để so sánh giá trị của hàm heuristic 
        if self.compute_heuristic() < other.compute_heuristic(): # Nếu giá trị heuristic hiện tại nhỏ hơn giá trị heuristic khác thì trả về True
            return True
        else: # Ngươc lại sẽ trả về False
            return False

# Hàm kiểm tra xem các điểm cần kiểm tra đã được phủ bởi các hộp hay chưa
def check_win(board, list_check_point):
    for p in list_check_point: # Duyệt tất cả các điểm có trong danh sách điểm cần kiểm tra
        if board[p[0]][p[1]] != '$': # Với mỗi điểm đó dóng sang ma trận bản đồ
            return False # Nếu như điểm đó chưa được phủ bới 1 hộp thì trả về False (Vẫn phải tiếp tục di chuyển các hộp để phủ hết các điểm)
    return True # Nếu như tất cả các điểm cần kiếm tra của ma trận bản đồ đều được phủ bởi 1 hộp thì trả về True

# Tìm vị trí hiện tại của player trong ma trận bản đồ
def find_position_player(board):
    for x in range(len(board)): # Duyêt tất cà các ô của ma trận bản đồ
        for y in range(len(board[0])):
            if board[x][y] == '@': # Nếu như có ô nào là player thì trả về vị trí hiện tại của ô đó
                return (x, y)
    return (-1, -1)  # Nếu không tìm thấy vị trí player thì trả về vị trí đặc biệt (bảng lỗi không có player để đẩy hộp)

# Kiểm tra xem 2 ma trận bản đồ có giống nhau hay không
def compare_matrix(board_A, board_B):
    if len(board_A) != len(board_B) or len(board_A[0]) != len(board_B[0]):
        return False # Nếu như 2 ma trạn bản đồ không có cùng kích thước => chúng không giống nhau
    for i in range(len(board_A)):
        for j in range(len(board_A[0])): # Duyệt tất cả các ô của ma trận bản đồ A
            if board_A[i][j] != board_B[i][j]:
                return False # Nếu phát hiện vị trí tương ứng của 2 ma trận bản đều khác nhau sẽ trả về False
    return True # Nếu như 2 ma trận bản đồ giống nhau thì trả về True

# Kiểm tra trạng thái với ma trận board đã tồn tịa trong danh sách list_state hay chưa
def is_board_exist(board, list_state):
    for state in list_state: # Duyệt tất cả các ma trận bản đồ có trong danh sách
        if compare_matrix(state.board, board): # Sử dụng hàm so sánh bên trên, nếu như board đã nằm trong danh sách thì  trả về True
            return True
    return False # Ngược lại không có trong danh sách thì sẽ trả về False

# Kiểm tra xem hộp đã nằm trên điểm cần kiểm tra hay chưa
def is_box_on_check_point(box, list_check_point):
    for check_point in list_check_point: # Duyệt hết tất cả các điểm cần kiểm tra trong danh sách
        if box[0] == check_point[0] and box[1] == check_point[1]: # Nếu như mà tọa độ của hộp bằng với tọa độ của điểm cần kiếm tra thì trả về True
            return True
    return False # Ngược lại nếu như hộp không nằm trên điểm cần kiểm tra thì trả về False

# Kiểm tra xem liệu 1 hộp có bị mắc kẹt trong góc tường hay không 
def check_in_corner(board, x, y, list_check_point): # Kiểm tra điểm (x,y) trên bản đồ có bị mắc kẹt trong góc tường hay không
    if board[x-1][y-1] == '#': # Kiểm tra ô nằm ở góc trái trên có phải là tường không
        if board[x-1][y] == '#' and board[x][y-1] == '#': # Kiểm tra ô trên và ô bên trái có phải là tường không
            if not is_box_on_check_point((x, y), list_check_point): # Nếu như ô cần kiểm tra mắc kẹt trong góc và đã nằm trên điểm cần kiểm tra thì trả về True
                return True
    if board[x+1][y-1] == '#': # Kiểm tra ô nằm ở góc trái dưới có phải là tường không
        if board[x+1][y] == '#' and board[x][y-1] == '#': # Kiểm tra ô dưới và ô bên trái có phải là tường không
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    if board[x-1][y+1] == '#': # Kiểm tra ô nằm ở góc phải trên có phải là tường không
        if board[x-1][y] == '#' and board[x][y+1] == '#': # Kiểm tra ô trên và ô bên phải có phải là tường không
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    if board[x+1][y+1] == '#': # Kiểm tra ô nằm ở góc phải dưới có phải là tường không
        if board[x+1][y] == '#' and board[x][y+1] == '#': # Kiểm tra ô dưới và ô bên phải có phải là tường không
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    return False # Nếu không nằm trên điểm cần kiểm tra thì ô đó đã bị mắc kẹt

# Tìm vị trí tất cả các hộp trong ma trận bản đồ
def find_boxes_position(board):
    result = [] # Danh sách chứa tọa độ của các hộp
    for i in range(len(board)):
        for j in range(len(board[0])): # Chạy 2 vòng for để có thể lấy hết các vị trí của các hộp
            if board[i][j] == '$': # Nếu tìm thấy các ô chứa hộp (có giá trị $)
                result.append((i, j)) # Thêm tọa độ vào danh sách
    return result # Trả về danh sách tọa độ các hộp 

# Kiểm tra xem 1 ô trên bản đồ có thể di chuyển hay không
def is_box_can_be_moved(board, box_position): # Xét ma trận bản đồ và hộp cần xét
    left_move = (box_position[0], box_position[1] - 1) # Ô bên trái của hộp
    right_move = (box_position[0], box_position[1] + 1) # Ô bên phải của hộp
    up_move = (box_position[0] - 1, box_position[1]) # Ô bên trên của hộp
    down_move = (box_position[0] + 1, box_position[1]) # Ô bên dưới của hộp
    # Nếu như ô bên trái của hộp (là khoảng trắng hoặc điểm cần kiểm tra hoặc player) và ô bên phải của hộp khác tường và khác hộp
    if (board[left_move[0]][left_move[1]] == ' ' or board[left_move[0]][left_move[1]] == '%' or board[left_move[0]][left_move[1]] == '@') and board[right_move[0]][right_move[1]] != '#' and board[right_move[0]][right_move[1]] != '$':
        return True # Trả về True (hộp có thể di chuyển ra vị trí khác)
    # Nếu như ô bên phải của hộp (là khoảng trắng hoặc điểm cần kiểm tra hoặc player) và ô bên trái của hộp khác tường và khác hộp
    if (board[right_move[0]][right_move[1]] == ' ' or board[right_move[0]][right_move[1]] == '%' or board[right_move[0]][right_move[1]] == '@') and board[left_move[0]][left_move[1]] != '#' and board[left_move[0]][left_move[1]] != '$':
        return True
    # Nếu như ô bên trên của hộp (là khoảng trắng hoặc điểm cần kiểm tra hoặc player) và ô bên dưới của hộp khác tường và khác hộp
    if (board[up_move[0]][up_move[1]] == ' ' or board[up_move[0]][up_move[1]] == '%' or board[up_move[0]][up_move[1]] == '@') and board[down_move[0]][down_move[1]] != '#' and board[down_move[0]][down_move[1]] != '$':
        return True
    # Nếu như ô bên dưới của hộp (là khoảng trắng hoặc điểm cần kiểm tra hoặc player) và ô bên trên của hộp khác tường và khác hộp
    if (board[down_move[0]][down_move[1]] == ' ' or board[down_move[0]][down_move[1]] == '%' or board[down_move[0]][down_move[1]] == '@') and board[up_move[0]][up_move[1]] != '#' and board[up_move[0]][up_move[1]] != '$':
        return True
    return False # Trả về False nếu như ô đó không thể di chuyển được nữa

# Kiểm tra xem tất cả các hộp trong ma trận có tồn tại có bị mắc kẹt và chưa nằm trên điểm cần kiểm tra hay chưa
def is_all_boxes_stuck(board, list_check_point):
    box_positions = find_boxes_position(board) # Lấy vị trí của tất cả các hộp trong ma trận bản đồ board 
    result = True
    for box_position in box_positions: # Duyệt tất cả các hộp có trong danh sách
        if is_box_on_check_point(box_position, list_check_point): # Nếu như hộp đã nằm trên điểm cần kiểm tra thì trả về False (vì ô đó đã nằm đúng điểm cần kiểm tra)
            return False
        if is_box_can_be_moved(board, box_position): # Nếu như hộp có thể di chuyển được thì trả về False (vì vẫn còn cách di chuyển ô đến mục tiêu)
            result = False
    return result # Nếu như có tồn tại ô bị mắc kẹt và không nằm trên điểm cần kiểm tra thì trả về True

# Kiểm tra xem trên bản đồ có hộp nào mắc kẹt ở góc tường hay không (không thể giải game vì không thể đẩy hộp đến vị trí cần kiểm tra)
def is_board_can_not_win(board, list_check_point):
    for x in range(len(board)):
        for y in range(len(board[0])): # Duyệt tất cả các ô cso trong ma trận bản đồ
            if board[x][y] == '$': # Nếu có ô nào là hộp 
                if check_in_corner(board, x, y, list_check_point): # Kiểm tra xem ô đó có bị mắc kẹt trong góc tường hay không
                    return True # Nếu có ô bị mắc kẹt thì trả về True (không thể giải game)
    return False # Nếu như không có ô nào mắc kẹt thì có thể tiếp tục di chuyển các ô đến điểm cần kiểm tra

# Trả về danh sách các vị trí mà player có thể di chuyển đến từ vị trí hiện tại
def get_next_pos(board, cur_pos): # xét ma trận và vị trí hiện tại của player
    '''return list of positions that player can move to from current position'''
    x, y = cur_pos[0], cur_pos[1] # Tọa độ của player hiện tại
    list_can_move = [] # Danh sách lưu các vị trí mà player có thể di chuyển từ vị trí hiện tại
    # Di chuyển lên trên với tọa độ mới (x-1,y)
    if 0 <= x - 1 < len(board): # Nếu như ô player di chuyển đến có nằm trong ma trận bản đồ
        value = board[x - 1][y] # Lưu giá trị ô mà player cần chuyển đến để so sánh
        if value == ' ' or value == '%': # Nếu như ô cần di chuyên đến là khảng trắng hoặc điểm cần kiểm tra thì player có thể đi qua
            list_can_move.append((x - 1, y)) # Thêm vị trí mà player có thể di chuyển đến
        elif value == '$' and 0 <= x - 2 < len(board): # Nếu như ô player cần di chuyển đến là hộp và vị trí bên trên của hộp tồn tại trong ma trận bản đồ
            next_pos_box = board[x - 2][y] # Lưu vị trí bên trên của hộp để kiểm tra
            if next_pos_box != '#' and next_pos_box != '$': # Nếu như vị trí đó không phải là tường và hộp
                list_can_move.append((x - 1, y)) # thì player có thể đẩy hộp lên vị trí đó và player sẽ thay thế đc vị trí hộp ban đầu
    # Di chuyển xuống dưới với tọa độ mới (x+1,y)
    if 0 <= x + 1 < len(board):
        value = board[x + 1][y]
        if value == ' ' or value == '%':
            list_can_move.append((x + 1, y))
        elif value == '$' and 0 <= x + 2 < len(board): # Nếu như ô player cần di chuyển đến là hộp và vị trí bên dưới của hộp tồn tại trong ma trận bản đồ
            next_pos_box = board[x + 2][y] # Lưu vị trí bên dưới của hộp để liểm tra
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x + 1, y))
    # Di chuyển sang trái với tọa độ mới (x,y-1)
    if 0 <= y - 1 < len(board[0]):
        value = board[x][y - 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y - 1))
        elif value == '$' and 0 <= y - 2 < len(board[0]): # Nếu như ô player cần di chuyển đến là hộp và vị trí bên trái của hộp tồn tại trong ma trận bản đồ
            next_pos_box = board[x][y - 2] # Lưu vị trí bên trái của hộp để kiểm tra
            if next_pos_box != '#' and next_pos_box != '$': # Nếu như vị trí đó không phải là tường và hộp
                list_can_move.append((x, y - 1)) # thì player có thể đẩy hộp lên vị trí đó và player sẽ thay thế đc vị trí hộp ban đầu
    # Di chuyển sang phải với tọa độ mới (x,y+!)
    if 0 <= y + 1 < len(board[0]):
        value = board[x][y + 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y + 1))
        elif value == '$' and 0 <= y + 2 < len(board[0]): # Nếu như ô player cần di chuyển đến là hộp và vị trí bên phải của hộp tồn tại trong ma trận bản đồ
            next_pos_box = board[x][y + 2] # Lưu vị trí bên phải của hộp để kiểm tra
            if next_pos_box != '#' and next_pos_box != '$': # Nếu như vị trí đó không phải là tường và hộp
                list_can_move.append((x, y + 1)) # thì player có thể đẩy hộp lên vị trí đó và player sẽ thay thế đc vị trí hộp ban đầu
    return list_can_move

# Thực hiện gán lại ma trận bản đồ hiện tại
def assign_matrix(board):
    return [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))] # Trả về ma trận bản đồ hiện tại

# Tao ra một ma trận bản đồ mới sau khi di chuyển
def move(board, next_pos, cur_pos, list_check_point):
    # Gán lại ma trận bản đồ hiện tại vào một ma trận bản đồ mới
    new_board = assign_matrix(board)
    # Tìm vị trí tiếp theo của hộp nếu player đẩy hộp
    if new_board[next_pos[0]][next_pos[1]] == '$': # Nếu như ô tiếp theo là ô chưa hộp thì cần xác định lại vị mới của hoppj sau khi đc đấy bởi player
        x = 2*next_pos[0] - cur_pos[0] # Tọa độ mới mà ô sẽ di chuyển đến
        y = 2*next_pos[1] - cur_pos[1]
        new_board[x][y] = '$' # Cập nhật lại ô mới cho bản đồ
    new_board[next_pos[0]][next_pos[1]] = '@' # Di chuyển player đến vị trí mới 
    new_board[cur_pos[0]][cur_pos[1]] = ' ' # Khi di chuyển player đến vị trí mới thì vị trí cũ cần gán lại là khoẳng trắng (ô mà player có thể đi quá)
    # Kiểm tra xem vị trí của các điểm kiểm tra trên bảng có trống hay không
    for p in list_check_point: # Duyệt tất cả các điểm có trong danh sách điểm cần kiểm tra
        if new_board[p[0]][p[1]] == ' ': # Nếu như vị trí đó còn trống 
            new_board[p[0]][p[1]] = '%' # Thì nó sẽ đặt lại điểm cần kiểm tra để biết rằng vị trí đó cần đặt hộp lên 
    return new_board # Trả về bản đồ mới sau khi di chuyển

# Tìm tất cả các điểm cần kiểm tra có trên ma trận bản đồ
def find_list_check_point(board):
    # Trả về danh sách điểm kiểm tra trên bản đồ nếu không có điểm kiểm tra nào trả về danh sách trống nó sẽ kiểm tra số hộp
    # nếu số hộp < số điểm kiểm tra trả về danh sách [(-1,-1)]
    list_check_point = [] # Tạo danh sách để lưu lại vị trí các ô cần kiểm tra
    num_of_box = 0 # Biến này dùng để đếm số hộp có trên màn hình
    for x in range(len(board)): # Kiểm tra toàn bộ vị trí của ma trận để tìm điểm cần kiểm tra và số hộp
        for y in range(len(board[0])):
            if board[x][y] == '$': # Nếu như đó là hộp thì tăng biến đếm hộp lên 1
                num_of_box += 1
            elif board[x][y] == '%': # Nếu như đó là điểm cần kiếm tra thì thêm vào danh sách vị trí các ô cần kiểm tra
                list_check_point.append((x, y))
    if num_of_box < len(list_check_point): # Nếu như số lượng hộp nhỏ hơn số lượng vị trí cần kiểm tra
        return [(-1, -1)] # Trả về giá trị đặc biệt (dùng để chi ra ma trận bản đồ không hợp lệ và không thể giải quyết)
    return list_check_point # Nếu không, hàm sẽ trả về danh sách các điểm cần kiểm tra đã tìm thấy ở ma trận bản đồ