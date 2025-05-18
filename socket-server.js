const express = require('express');
const http = require('http');
const cors = require('cors');
const { Server } = require('socket.io');

const app = express();
app.use(cors());

const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: '*',
    methods: ['GET', 'POST']
  }
});

const roomUsers = {}; // Optional tracking

io.on('connection', socket => {
  console.log('🟢 New client connected:', socket.id);

  socket.on('join-room', joinCode => {
    socket.join(joinCode);
    console.log(`📥 ${socket.id} joined room ${joinCode}`);
    socket.to(joinCode).emit('ready', { peerId: socket.id });

    roomUsers[joinCode] = roomUsers[joinCode] || [];
    roomUsers[joinCode].push(socket.id);
  });
  socket.on('class-live', ({ joinCode }) => {
  socket.to(joinCode).emit('class-live');
});

socket.on('class-ended', ({ joinCode }) => {
  socket.to(joinCode).emit('class-ended');
});


  socket.on('signal', ({ to, signal }) => {
    io.to(to).emit('instructor-signal', { signal, from: socket.id });
  });

  socket.on('return-signal', ({ to, signal }) => {
    io.to(to).emit('signal', { signal, from: socket.id });
  });

  socket.on('student-joined', ({ joinCode, name, recognized }) => {
    console.log(`👥 ${name} has joined ${joinCode} — ${recognized ? '✅ recognized' : '⚠️ unrecognized'}`);
    socket.to(joinCode).emit('student-joined', { name, recognized });
  });

  socket.on('disconnect', () => {
    console.log('🔌 Client disconnected:', socket.id);
    for (const room of socket.rooms) {
      if (room !== socket.id) {
        socket.to(room).emit('user-disconnected', socket.id);
        if (roomUsers[room]) {
          roomUsers[room] = roomUsers[room].filter(id => id !== socket.id);
        }
      }
    }
  });
});

app.get('/', (req, res) => res.send('Socket.IO server is running ✅'));

server.listen(8001, () => {
  console.log('✅ Socket.IO server running at http://localhost:8001');
});
