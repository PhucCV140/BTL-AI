import support_function as spf # import module support_function và đặt tên ngắn gọn cho nó là spf
import time # Sử dụng để đo thời gian trong chương trình
from queue import PriorityQueue # Gọi class PriorityQueue trong module queue để lưu trữ các trạng thái được sinh ra
# Triển khai thuật toán A*
def AStart_Search(board, list_check_point):#với đầu vào là bảng trò chơi (board) và danh sách các checkpoint (list_check_point).
    start_time = time.time() # Ghi nhận thời điểm bắt đầu tính toán
    if spf.check_win(board,list_check_point):#check trạng thái hiện tại là win hàm sẽ in ra "Found win"
        print("Found win")
        return [board] # trả về danh sách trạng thái gồm các trạng thái đầu vào
    start_state = spf.state(board, None, list_check_point) #khởi tạo một đối tượng "state" đại diện cho trạng thái ban đầu của trò chơi
    list_state = [start_state] #khởi tạo một danh sách các trạng thái đã được xét qua trong quá trình giải thuật A*
    heuristic_queue = PriorityQueue() #khởi tạo một hàng đợi ưu tiên (PriorityQueue) để lưu trữ các trạng thái được sinh ra trong quá trình giải thuật A*
    heuristic_queue.put(start_state) # thêm trạng thái ban đầu (start_state) vào hàng đợi ưu tiên (heuristic_queue)
    while not heuristic_queue.empty():#Vòng lặp sẽ tiếp tục cho đến khi hàng đợi ưu tiên (heuristic_queue)  không còn phần tử nào
        now_state = heuristic_queue.get()#lấy phần tử đầu tiên trong hàng đợi ưu tiên (heuristic_queue) và gán vào biến now_state.
        cur_pos = spf.find_position_player(now_state.board)# tìm vị trí của người chơi trên bản đồ (board) trong trạng thái hiện tại (now_state)
        #Hàm find_position_player sẽ trả về tọa độ (dòng, cột) của ô chứa người chơi. Biến cur_pos sẽ lưu trữ kết quả trả về từ hàm này.
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)#tìm các vị trí tiếp theo mà người chơi có thể đi tới từ vị trí hiện tại (cur_pos) trên bản đồ (board) trong trạng thái hiện tại (now_state). Hàm get_next_pos sẽ trả về danh sách các tọa độ (dòng, cột) của các ô mà người chơi có thể đi tới. Biến list_can_move sẽ lưu trữ kết quả trả về từ hàm này.
        for next_pos in list_can_move:# thực hiện các bước xử lý trong mỗi vòng lặp của thuật toán A* để tìm đường đi ngắn nhất từ trạng thái hiện tại tới trạng thái kết thúc.
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)#Tạo một bản đồ mới (new_board) bằng cách di chuyển người chơi tới ô next_pos và cập nhật vị trí của ô cur_pos mà người chơi đang đứng trên bản đồ hiện tại.
            if spf.is_board_exist(new_board, list_state):#Kiểm tra xem trạng thái mới này đã xuất hiện trước đó hay chưa (is_board_exist)
                continue
            if spf.is_board_can_not_win(new_board, list_check_point):#Kiểm tra xem trên bản đồ mới này có khả năng thắng hay không
                continue
            if spf.is_all_boxes_stuck(new_board, list_check_point):#Kiểm tra xem tất cả các hộp trên bản đồ có bị kẹt không (is_all_boxes_stuck).
                continue
            new_state = spf.state(new_board, now_state, list_check_point)#Tạo một trạng thái mới (new_state) bằng cách đóng gói bản đồ mới new_board, trạng thái hiện tại now_state và danh sách các điểm kiểm tra list_check_point.
            if spf.check_win(new_board, list_check_point):#Nếu trạng thái mới này đã là trạng thái kết thúc (check_win), ta đã tìm thấy đường đi ngắn nhất
                print("Found win")
                return (new_state.get_line(), len(list_state))
            list_state.append(new_state)#Thêm trạng thái mới new_state vào danh sách trạng thái đã xét list_state.
            heuristic_queue.put(new_state)#Thêm trạng thái mới new_state vào hàng đợi ưu tiên heuristic_queue.
            end_time = time.time()#
            if end_time - start_time > spf.TIME_OUT:#Kiểm tra xem thời gian tính toán đã vượt quá giới hạn cho phép hay chưa (TIME_OUT).
                return []
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:#Nếu thời gian thực hiện vượt quá giá trị TIME_OUT, hàm sẽ trả về một list rỗng và kết thúc
            return []
    print("Not Found")#Nếu vòng lặp while đã chạy xong mà không tìm thấy kết quả, hàm sẽ in ra thông báo "Not Found" và trả về một list rỗng.
    return []