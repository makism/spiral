using System;
using System.Collections;
using System.Collections.Generic;


namespace spiral.ga
{
    public abstract class Genome<T>: Pool<T>
    {
        #region Members
        protected float fitness;

        protected int size;

        protected int id;

        private static int idCounter;

        protected bool isMutated;

        protected bool successCrossover;

        protected bool permutationEncoding;

        protected bool isCreated;

        protected static Random random = new Random();
        #endregion

        #region Properties
        public bool UsePermutationEncoding
        {
            get { return permutationEncoding; }
            set { permutationEncoding = value; }
        }

        public float Fitness
        {
            get { return fitness; }
        }

        public int Size
        {
            get { return size; }
        }

        public int Id
        {
            get { return id; }
        }

        public bool IsMutated
        {
            get { return isMutated; }
        }

        public bool SuccessCrossover
        {
            get { return successCrossover; }
        }
        #endregion

        #region Ctors/Dtors
        public Genome()
            :base()
        {
            Init();
        }

        public Genome(int size)
            :base()
        {
            Init();
            this.size = size;

            Create();
        }

        public Genome(int size, bool permutation)
            : base()
        {
            Init();
            this.size = size;
            this.permutationEncoding = permutation;

            Create();
        }

        public Genome(int size, bool permutation, bool nocreate)
            : base()
        {
            Init();
            this.size = size;
            this.permutationEncoding = permutation;

            if (nocreate == false)
                Create();
        }
        #endregion

        protected void Init()
        {
            fitness = 0.0f;
            size = 0;
            id = ++idCounter;
            isMutated = false;
            successCrossover = false;
            permutationEncoding = false;
        }

        protected abstract void RandomEncoding();

        protected abstract void PermutationEncoding();

        public virtual void Create()
        {
            if (isCreated == false)
            {
                if (permutationEncoding)
                    PermutationEncoding();
                else
                    RandomEncoding();

                isCreated = true;
            }
        }

        public T[] ToArray()
        {
            return pool.ToArray();
        }

        #region Overriden methods
        public override string ToString()
        {
            string str = " #" + id;

            str += " (fitness: " + fitness + ") ";

            str += "[";
            for (int i = 0; i < size; i++)
            {
                str += this[i];

                if (i < size - 1)
                    str += " ";
            }
            str += "]";

            return str;
        }

        public override bool Equals(object obj)
        {
            return base.Equals(obj);
        }

        public override int GetHashCode()
        {
            return base.GetHashCode();
        }
        #endregion

        #region Operator overload
        public static bool operator !=(Genome<T> t1, Genome<T> t2)
        {
            return true;
        }

        public static bool operator==(Genome<T> t1, Genome<T> t2)
        {
            return true;
        }
        #endregion
    }
}
