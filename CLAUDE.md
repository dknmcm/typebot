# Human-Like Typing Bot Implementation Plan

## Working Preferences
**IMPORTANT:** Claude is only permitted to:
- Edit this CLAUDE.md file
- Provide suggestions and recommendations
- Analyze and plan implementations

**Claude must NEVER:**
- Implement any direct code changes
- Execute any commands
- Create any files other than this CLAUDE.md

All implementation work will be done manually by the user based on Claude's suggestions and plans.

## Project Overview
A system-level typing bot that reads text from screen using OCR and simulates 
human typing behavior to test typing test detection mechanisms. Uses macOS 
Quartz Events for keyboard simulation and Tesseract OCR for text recognition.

## Technical Architecture

### Core Components
1. **Screen Region Monitor** - Captures specific screen area continuously
2. **OCR Text Extractor** - Converts screenshots to text using Tesseract
3. **Human Behavior Engine** - Simulates realistic typing patterns and errors
4. **Keystroke Generator** - Sends keyboard events via macOS Quartz
5. **State Manager** - Tracks typing progress and text changes

## Dependencies & Tools
```
pytesseract>=0.3.10    # OCR text recognition
pillow>=9.0.0          # Image processing
pynput>=1.7.6          # macOS keyboard event generation
opencv-python>=4.8.0   # Image preprocessing
numpy>=1.24.0          # Mathematical operations
mss>=6.1.0             # Fast screenshot capture
tkinter                # GUI for region selection (built-in)
```

## Step-by-Step Implementation Plan

2. **Screen Region Selection Tool** (`screen_monitor.py`)
   - Create tkinter overlay for region selection
   - Allow user to drag-select text area on screen
   - Save coordinates for monitoring
   - Implement continuous screenshot capture using `mss`
   - Add change detection using image hashing

### Phase 2: OCR Implementation
3. **OCR Text Processor** (`ocr_processor.py`)
   - Install Tesseract: `brew install tesseract`
   - Implement image preprocessing pipeline:
     - Convert to grayscale
     - Increase contrast
     - Noise reduction
     - Scale up for better OCR accuracy
   - Configure Tesseract for English text recognition
   - Add confidence scoring and error handling
   - Implement text diffing to detect changes

### Phase 3: Human Behavior Simulation
4. **Behavior Engine** (`behavior_engine.py`)
   - **Timing Patterns:**
     - Normal distribution for inter-keystroke delays (mean: 120ms, std: 30ms)
     - Character-pair specific timing adjustments
     - Slower typing for uncommon letter combinations
   - **Error Generation:**
     - 2-5% error rate with character substitutions
     - Common typos (adjacent keys, doubled letters)
     - Realistic correction patterns (immediate backspace vs delayed)
   - **Fatigue Simulation:**
     - Gradual speed decrease over time
     - Occasional longer pauses (500-2000ms)
     - WPM variation (±10-20% from baseline)

5. **Keystroke Generator** (`keystroke_generator.py`)
   - Use `pynput.keyboard.Controller` for macOS Quartz events
   - Implement proper key press/release timing
   - Add natural key hold duration variation (50-150ms)
   - Handle special characters and modifiers
   - Include subtle mouse micro-movements during typing

### Phase 4: State Management
6. **State Manager** (`state_manager.py`)
   - Track current typing position in text
   - Handle text updates mid-typing
   - Manage typing queue and corrections
   - Implement pause/resume functionality
   - Add session statistics tracking

### Phase 5: Integration & Testing
7. **Main Application** (`main.py`)
   - GUI for configuration and control
   - Start/stop typing automation
   - Real-time status display
   - Settings for behavior parameters

8. **Configuration System** (`config.py`)
   - Adjustable typing speed (30-80 WPM)
   - Error rate settings (0-10%)
   - Behavior randomness levels
   - OCR sensitivity settings

### Phase 6: Anti-Detection Features
9. **Advanced Behavior Patterns**
   - Random session start delays
   - Realistic break patterns
   - Natural reading pauses before typing
   - Occasional re-reading (cursor position changes)

10. **Performance Optimization**
    - Efficient image processing pipeline
    - Smart OCR triggering (only on text changes)
    - Memory usage optimization
    - CPU usage monitoring

## Implementation Sequence

### Week 1: Foundation
- Set up project structure and dependencies
- Implement screen region selection GUI
- Basic screenshot capture functionality
- Test OCR with simple text samples

### Week 2: Core Features
- Complete OCR integration with preprocessing
- Basic keystroke generation
- Simple timing patterns
- Text change detection

### Week 3: Human Behavior
- Advanced timing models
- Error generation and correction
- Fatigue simulation
- State management

### Week 4: Testing & Refinement
- Test on typing websites (monkeytype.com, typeracer.com)
- Performance optimization
- Anti-detection feature implementation
- Documentation and configuration options

## Testing Strategy
1. **Unit Testing:** Each component individually
2. **Integration Testing:** Full pipeline with sample text
3. **Real-world Testing:** Against actual typing test websites
4. **Detection Testing:** Monitor for any automation detection
5. **Performance Testing:** CPU/memory usage under continuous operation

## Security Considerations
- This tool is for defensive security research only
- Ensure proper disclosure if used in academic research
- Consider rate limiting to avoid service disruption
- Implement safeguards against misuse

## Success Metrics
- Undetectable by common bot detection mechanisms
- Realistic typing patterns that pass human analysis
- Consistent performance across different websites
- Configurable behavior for various testing scenarios