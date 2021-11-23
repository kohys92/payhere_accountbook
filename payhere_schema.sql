CREATE TABLE `users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `email` varchar(255),
  `password` varchar(255),
  `last_name` varchar(255),
  `first_name` varchar(255),
  `created_at` date,
  `updated_at` date
);

CREATE TABLE `ledgers` (
  `id` int AUTO_INCREMENT,
  `note` varchar(255),
  `created_at` date,
  `income` int,
  `expense` int,
  `total_income` int,
  `total_expense` int,
  `category` varchar(255),
  `is_removed` boolean,
  `user_id` int
);

ALTER TABLE `ledgers` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
