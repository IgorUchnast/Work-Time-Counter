import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

class TaskDetailsPage extends StatefulWidget {
  final Map task;

  const TaskDetailsPage({super.key, required this.task});

  @override
  // ignore: library_private_types_in_public_api
  _TaskDetailsPageState createState() => _TaskDetailsPageState();
}

class _TaskDetailsPageState extends State<TaskDetailsPage> {
  bool isWorking = false;
  bool isOnBreak = false;
  Timer? timer;
  int workTime = 0;
  int breakTime = 0;

  void startTask() async {
    setState(() {
      isWorking = true;
      isOnBreak = false;
    });

    await http.post(
      Uri.parse('http://127.0.0.1:5000/employee/1/task_status'),
      headers: {'Content-Type': 'application/json'},
      body:
          json.encode({'task_id': widget.task['task_id'], 'task_start': true}),
    );

    timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      setState(() {
        workTime++;
      });
    });
  }

  void stopTask() async {
    timer?.cancel();

    // Wysyłanie POST do data_aggregation
    await http.post(
      Uri.parse('http://127.0.0.1:5000/employee/1/work_time'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'task_id': widget.task['task_id'],
        'work_time': workTime,
        'break_time': breakTime,
      }),
    );

    // Wysyłanie POST do task_status
    await http.post(
      Uri.parse('http://127.0.0.1:5000/employee/1/task_status'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'task_id': widget.task['task_id'],
        'task_stop': true, // Informacja o zakończeniu zadania
      }),
    );

    setState(() {
      isWorking = false;
      isOnBreak = false;
      workTime = 0;
      breakTime = 0;
    });
  }

  void takeBreak() {
    timer?.cancel();
    setState(() {
      isWorking = false;
      isOnBreak = true;
    });

    timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      setState(() {
        breakTime++;
      });
    });
  }

  void continueTask() {
    timer?.cancel();
    setState(() {
      isWorking = true;
      isOnBreak = false;
    });

    timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      setState(() {
        workTime++;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          widget.task['name'],
          style: const TextStyle(color: Colors.white),
        ),
        backgroundColor: const Color.fromARGB(255, 0, 25, 45),
      ),
      body: Container(
        width: double.infinity,
        decoration: const BoxDecoration(
          color: Color.fromARGB(255, 0, 25, 45),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Work Time: ${Duration(seconds: workTime).inMinutes}:${(workTime % 60).toString().padLeft(2, '0')}',
              style: const TextStyle(fontSize: 24, color: Colors.white),
            ),
            Text(
              'Break Time: ${Duration(seconds: breakTime).inMinutes}:${(breakTime % 60).toString().padLeft(2, '0')}',
              style: const TextStyle(fontSize: 24, color: Colors.white),
            ),
            const SizedBox(height: 20),
            if (!isWorking && !isOnBreak)
              ElevatedButton(
                onPressed: startTask,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.green,
                  minimumSize:
                      const Size(150, 150), // szerokość: 150, wysokość: 50
                  padding: const EdgeInsets.symmetric(
                    horizontal: 20,
                    vertical: 10,
                  ), // dodatkowe marginesy wewnętrzne
                ),
                child: const Text(
                  'Start',
                  style:
                      TextStyle(fontSize: 25), // zwiększenie rozmiaru czcionki
                ),
              ),
            if (isWorking)
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  ElevatedButton(
                    onPressed: stopTask,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.red,
                      minimumSize:
                          const Size(150, 150), // szerokość: 150, wysokość: 50
                      padding: const EdgeInsets.symmetric(
                        horizontal: 20,
                        vertical: 10,
                      ), // dodatkowe marginesy wewnętrzne
                    ),
                    child: const Text(
                      'Stop',
                      style: TextStyle(color: Colors.white, fontSize: 25),
                    ),
                  ),
                  ElevatedButton(
                    onPressed: takeBreak,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.black,
                      minimumSize:
                          const Size(150, 150), // szerokość: 150, wysokość: 50
                      padding: const EdgeInsets.symmetric(
                        horizontal: 20,
                        vertical: 10,
                      ), // dodatkowe marginesy wewnętrzne
                    ),
                    child: const Text(
                      'Break',
                      style: TextStyle(color: Colors.white, fontSize: 25),
                    ),
                  ),
                ],
              ),
            if (isOnBreak)
              ElevatedButton(
                onPressed: continueTask,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.orange,
                  minimumSize:
                      const Size(150, 150), // szerokość: 150, wysokość: 50
                  padding: const EdgeInsets.symmetric(
                    horizontal: 20,
                    vertical: 10,
                  ), // dodatkowe marginesy wewnętrzne
                ),
                child: const Text(
                  'Continue',
                  style: TextStyle(color: Colors.white, fontSize: 25),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
