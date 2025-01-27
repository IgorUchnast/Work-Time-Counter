// import 'package:flutter/material.dart';
// import 'dart:async';
// import 'dart:convert';
// import 'package:http/http.dart' as http;
// import 'package:work_timer/pages/task_details_page.dart';

// class HomePage extends StatefulWidget {
//   const HomePage({super.key});

//   @override
//   // ignore: library_private_types_in_public_api
//   _HomePageState createState() => _HomePageState();
// }

// class _HomePageState extends State<HomePage> {
//   List tasks = [];

//   Future<void> fetchTasks() async {
//     final response = await http
//         .get(Uri.parse('http://127.0.0.1:5000/employee/1/task_assignments'));
//     if (response.statusCode == 200) {
//       setState(() {
//         tasks = json.decode(response.body);
//       });
//     } else {
//       throw Exception('Failed to load tasks');
//     }
//   }

//   Future<void> fetchEmployee() async {
//     final response =
//         await http.get(Uri.parse('http://127.0.0.1:5000/employees'));
//     if (response.statusCode == 200) {
//       setState(() {
//         tasks = json.decode(response.body);
//       });
//     } else {
//       throw Exception('Failed to load tasks');
//     }
//   }

//   @override
//   void initState() {
//     super.initState();
//     fetchTasks();
//     fetchEmployee();
//   }

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(
//         backgroundColor: const Color.fromARGB(255, 0, 25, 45),
//         title: const Text(
//           'Tasks List',
//           style: TextStyle(color: Colors.white),
//         ),
//       ),
//       body: Container(
//         color: const Color.fromARGB(255, 0, 25, 45),
//         padding: const EdgeInsets.all(5),
//         child: tasks.isEmpty
//             ? const Center(child: CircularProgressIndicator())
//             : ListView.builder(
//                 itemCount: tasks.length,
//                 itemBuilder: (context, index) {
//                   return Container(
//                     padding: const EdgeInsets.all(10),
//                     margin: const EdgeInsets.all(10),
//                     decoration: const BoxDecoration(
//                       color: Color.fromARGB(255, 4, 43, 76),
//                     ),
//                     child: ListTile(
//                       title: Text(
//                         tasks[index]['name'],
//                         style: const TextStyle(color: Colors.white),
//                       ),
//                       subtitle: Text(
//                         tasks[index]['project_name'],
//                         style: const TextStyle(color: Colors.white),
//                       ),
//                       onTap: () {
//                         Navigator.push(
//                           context,
//                           MaterialPageRoute(
//                             builder: (context) =>
//                                 TaskDetailsPage(task: tasks[index]),
//                           ),
//                         );
//                       },
//                     ),
//                   );
//                 },
//               ),
//       ),
//     );
//   }
// }

import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:work_timer/pages/task_details_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List tasks = [];
  List employees = [];
  int? selectedEmployeeId;

  Future<void> fetchTasks(int employeeId) async {
    final response = await http.get(Uri.parse(
        'http://127.0.0.1:5000/employee/$employeeId/task_assignments'));
    if (response.statusCode == 200) {
      setState(() {
        tasks = json.decode(response.body);
      });
    } else {
      throw Exception('Failed to load tasks');
    }
  }

  Future<void> fetchEmployees() async {
    final response =
        await http.get(Uri.parse('http://127.0.0.1:5000/employees'));
    if (response.statusCode == 200) {
      setState(() {
        employees = json.decode(response.body);
      });
    } else {
      throw Exception('Failed to load employees');
    }
  }

  @override
  void initState() {
    super.initState();
    fetchEmployees(); // Pobranie listy pracowników przy starcie aplikacji
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color.fromARGB(255, 0, 25, 45),
        title: const Text(
          'Tasks List',
          style: TextStyle(color: Colors.white),
        ),
      ),
      drawer: Drawer(
        child: employees.isEmpty
            ? const Center(child: CircularProgressIndicator())
            : ListView.builder(
                itemCount: employees.length,
                itemBuilder: (context, index) {
                  final employee = employees[index];
                  return ListTile(
                    title: Text(
                        '${employee['first_name']} ${employee['last_name']}'),
                    subtitle: Text(employee['position']),
                    onTap: () {
                      setState(() {
                        selectedEmployeeId = employee['employee_id'];
                      });
                      Navigator.pop(context); // Zamknięcie Drawer
                      fetchTasks(employee[
                          'employee_id']); // Pobranie zadań dla wybranego pracownika
                    },
                  );
                },
              ),
      ),
      body: Container(
        color: const Color.fromARGB(255, 0, 25, 45),
        padding: const EdgeInsets.all(5),
        child: tasks.isEmpty
            ? const Center(child: CircularProgressIndicator())
            : ListView.builder(
                itemCount: tasks.length,
                itemBuilder: (context, index) {
                  return Container(
                    padding: const EdgeInsets.all(10),
                    margin: const EdgeInsets.all(10),
                    decoration: const BoxDecoration(
                      color: Color.fromARGB(255, 4, 43, 76),
                    ),
                    child: ListTile(
                      title: Text(
                        tasks[index]['name'],
                        style: const TextStyle(color: Colors.white),
                      ),
                      subtitle: Text(
                        tasks[index]['project_name'],
                        style: const TextStyle(color: Colors.white),
                      ),
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => TaskDetailsPage(
                              task: tasks[index],
                              employeeId: selectedEmployeeId ?? 1,
                            ),
                          ),
                        );
                      },
                    ),
                  );
                },
              ),
      ),
    );
  }
}
