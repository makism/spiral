using System;
using System.Collections;
using System.Collections.Generic;


namespace spiral.ga
{
    public class Population
    {
        private int id;

        private string name;

        private static int idCounter;

        private ArrayList pool;


        public Population()
        {
            id = ++idCounter;
            name = "";
        }

        public Population(int id, string name)
        {
            this.id = id;
            this.name = name;
        }

        public override string ToString()
        {
            return base.ToString();
        }
    }
}
