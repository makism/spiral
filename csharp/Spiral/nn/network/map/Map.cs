using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace spiral.ga.nn.network.map
{
    public abstract class Map
    {

        public Map()
        {

        }

        public abstract void Init();

        public abstract void Learn();

    }
}
