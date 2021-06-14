from csvtodb.Csv import Csv
from csvtodb.LaravelTable import LaravelTable


class Laravel(LaravelTable):
    def __repr__(self):
        return 'build seeder and table migration files for laravel from csv'

    @classmethod
    def new_migration(cls, csv: Csv, filepath: str, filename: str, engine: str = 'InnoDB',
                      temporary: bool = False) -> bool:
        """
        build new migration file for laravel

        order step :\n
        - create your migration file with your laravel
        - set new csv with the csv class
        - call this method
        - run program

         your migration is now build congrats !\n

         **csv:**\n
         the csv you initialize before\n

         **filepath:**\n
         the path to the migration folder in your Laravel (absolute path recommended to avoid errors)\n

         **filename:**\n
         the name of your migration file create in your Laravel\n

         **engine:**\n
         engine you want to use for your table\n

         **temporary:**\n
         if your table need to be temporary set it to True\n

        :param csv: Csv
        :param filepath: str
        :param filename: str
        :param engine: str
        :param temporary: bool
        :return: bool
        """
        migration = '<?php\n\n' \
                    'use Illuminate\\Database\\Migrations\\Migration;\n' \
                    'use Illuminate\\Database\\Schema\\Blueprint;\n' \
                    'use Illuminate\\Support\\Facades\\Schema;\n\n' \
                    f'class {csv.p_filename} extends Migration\n' \
                    '{\n' \
                    '\tpublic function up()\n\t{'
        migration += cls._build_table(csv=csv, engine=engine, temporary=temporary)
        migration += '\t}\n\n'
        migration += '\tpublic function down()\n\t{\n'
        migration += cls._down(csv=csv)
        migration += '\t}\n'
        migration += '}\n'

        try:
            with open(f'{filepath}/{filename}.php', 'x') as file:
                file.write(migration)
            file.close()
        except FileExistsError:
            with open(f'{filepath}/{filename}.php', 'w') as file:
                file.write(migration)
            file.close()
        return True

    @classmethod
    def new_seeder(cls, csv: Csv, filepath: str, filename: str) -> bool:
        """
        build new seeder for laravel

        :param csv: Csv
        :param filepath: str
        :param filename: str
        :return: str
        """
        column_name = csv.column_name()
        content = csv.row_list()
        seeder = '<?php\n\n' \
                 'namespace Database\\Seeders;\n\n' \
                 'use Illuminate\\Database\\Seeder;\n' \
                 'use Illuminate\\Support\\Facades\\DB;\n\n' \
                 f'class {filename} extends Seeder\n' \
                 '{\n' \
                 '\tpublic function run()\n' \
                 '\t{\n' \
                 f'\t\tDB::table("{csv.p_filename}")->insert([\n' \

        for i in range(0, len(content)):
            seeder += '\t\t\t[\n'
            for j in range(0, len(content[i])):
                    seeder += f'\t\t\t\t"{column_name[j]}" => "{content[i][j]}",\n'
            seeder += '\t\t\t]\n' if i == len(content)-1 else '\t\t\t],\n'

        seeder += '\t\t]);\n' \
                  '\t}\n' \
                  '}'
        try:
            with open(f'{filepath}/{filename}.php', 'w') as file:
                file.write(seeder)
            file.close()
            return True
        except Exception as e:
            print(e)
            return False
