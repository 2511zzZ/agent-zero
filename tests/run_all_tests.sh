#!/bin/bash

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🚀 Agent Zero Board Testing Suite${NC}"
echo -e "${PURPLE}====================================${NC}"

# 记录开始时间
START_TIME=$(date +%s)

# 设置Python路径
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 1. 生成测试数据
echo -e "\n${BLUE}📊 Step 1: Generating test data...${NC}"
echo -e "${CYAN}Running: python tests/generate_test_data.py${NC}"

if python tests/generate_test_data.py; then
    echo -e "${GREEN}✅ Test data generated successfully${NC}"
else
    echo -e "${RED}❌ Failed to generate test data${NC}"
    exit 1
fi

# 2. 测试board_output工具
echo -e "\n${BLUE}🧪 Step 2: Testing board_output enhanced tool...${NC}"
echo -e "${CYAN}Running: python tests/test_board_output.py${NC}"

if python tests/test_board_output.py; then
    echo -e "${GREEN}✅ Board output tool tests passed${NC}"
else
    echo -e "${RED}❌ Board output tool tests failed${NC}"
    echo -e "${YELLOW}⚠️  Continuing with other tests...${NC}"
fi

# 3. 验证测试数据文件
echo -e "\n${BLUE}📋 Step 3: Verifying test data files...${NC}"

TEST_FILES=("simple_project" "complex_project" "mixed_nodes" "stress_test")
for file in "${TEST_FILES[@]}"; do
    filepath="tests/data/board_${file}.json"
    if [ -f "$filepath" ]; then
        filesize=$(stat -f%z "$filepath" 2>/dev/null || stat -c%s "$filepath" 2>/dev/null || echo "0")
        echo -e "${GREEN}✅ ${filepath} (${filesize} bytes)${NC}"
    else
        echo -e "${RED}❌ Missing: ${filepath}${NC}"
    fi
done

# 4. 检查生成的board状态
echo -e "\n${BLUE}📄 Step 4: Checking generated board state...${NC}"

BOARD_FILE="memory/board_test_board.json"
if [ -f "$BOARD_FILE" ]; then
    echo -e "${GREEN}✅ Board state file found: ${BOARD_FILE}${NC}"
    
    # 显示board统计信息
    if command -v jq >/dev/null 2>&1; then
        echo -e "${CYAN}📊 Board Statistics:${NC}"
        echo -e "   Nodes: $(jq '.nodes | length' "$BOARD_FILE")"
        echo -e "   Connections: $(jq '.connections | length' "$BOARD_FILE")"
        echo -e "   Version: $(jq '.version' "$BOARD_FILE")"
        echo -e "   Title: $(jq -r '.metadata.title' "$BOARD_FILE")"
    else
        echo -e "${YELLOW}⚠️  jq not found, skipping JSON analysis${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Board state file not found${NC}"
fi

# 5. 启动可视化测试服务器
echo -e "\n${BLUE}🌐 Step 5: Starting visualization test server...${NC}"

# 检查Python HTTP服务器
if command -v python3 >/dev/null 2>&1; then
    echo -e "${CYAN}Starting Python HTTP server on port 8000...${NC}"
    echo -e "${GREEN}🌍 Test URLs:${NC}"
    echo -e "   Main test page: ${CYAN}http://localhost:8000/tests/board_test.html${NC}"
    echo -e "   Test data: ${CYAN}http://localhost:8000/tests/data/${NC}"
    echo ""
    echo -e "${YELLOW}📝 Instructions:${NC}"
    echo -e "   1. Open the test page in your browser"
    echo -e "   2. Click the scenario buttons to test visualization"
    echo -e "   3. Use the API test button to test backend connectivity"
    echo -e "   4. Try uploading custom JSON files"
    echo ""
    echo -e "${PURPLE}⌨️  Keyboard shortcuts:${NC}"
    echo -e "   Ctrl+1: Simple project"
    echo -e "   Ctrl+2: Complex project"
    echo -e "   Ctrl+3: Mixed nodes"
    echo -e "   Ctrl+4: Stress test"
    echo -e "   Ctrl+S: Export data"
    echo -e "   Ctrl+R: Clear board"
    echo ""
    echo -e "${BLUE}🔧 Development testing:${NC}"
    echo -e "   Board UI dev server: ${CYAN}http://localhost:3001${NC}"
    echo -e "   Main backend: ${CYAN}http://localhost:3000${NC}"
    echo ""
    
    # 启动服务器
    python3 -m http.server 8000 &
    SERVER_PID=$!
    
    echo -e "${GREEN}✅ HTTP server started with PID: $SERVER_PID${NC}"
    echo -e "${CYAN}Press Ctrl+C to stop the server and exit${NC}"
    
    # 设置信号处理
    trap "echo -e '\n${YELLOW}🛑 Stopping server...${NC}'; kill $SERVER_PID 2>/dev/null; echo -e '${GREEN}✅ Server stopped${NC}'; exit 0" INT
    
    # 等待用户中断
    wait $SERVER_PID
else
    echo -e "${RED}❌ Python3 not found. Please install Python3 to run the test server.${NC}"
fi

# 计算总耗时
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo -e "\n${PURPLE}🏁 Testing completed in ${DURATION} seconds${NC}"
echo -e "${GREEN}✅ All tests finished!${NC}"